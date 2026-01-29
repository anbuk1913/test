    https://overfruitfully-nondisinterested-dreama.ngrok-free.dev/
.

    import SectionPagination from "@/components/patient/common/UI/PaginationComponent";
    import { ThemeColors } from "@/constants/theme";
    import { useEffect, useState, useRef } from "react";
    import { useDispatch, useSelector } from "react-redux";
    import { useLocation, useNavigate } from "react-router-dom";
    import { LOCATION_API } from "@/api/location/locationApi";
    import AlertModal from "@/components/modal/AlertModal";
    import { ChevronDown, X } from "lucide-react";
    import { AppointmentMissingReason } from "@/redux/location/types";
    import { AddNewAppointmentMissingReason, RemoveAppointmentMissingReason } from "@/redux/location/PracticeLocationSlice";
    import { AppointmentsIcon } from "@/assets/svg/Icons";
    
    type ReasonType = 'missing' | 'cancel';
    
    const AppointmentMissingReasonSection = () => {
        const { PracticeLocationInfo, AppointmentMissingReasons } = useSelector((state: any) => state.practiceLocation);
        const { bgColor, appSecondaryClr } = ThemeColors;
        const location = useLocation();
        const dispatch = useDispatch();
        const navigate = useNavigate();
    
        console.log("LocationAppointmentReasons", AppointmentMissingReasons);
    
        const columns = [
            { key: "Sl:No", label: "Sl:No" },
            { key: "Date", label: "Date" },
            { key: "Time", label: "Time" },
            { key: "Reason", label: "Reason" },
        ];
    
        const rowActions = [
            { label: "Remove", onClick: (item: any) => confirmDelete(item.LocationReasonTypeId) },
        ];
    
        const [appointmentReasons, setAppointmentReasons] = useState<{ ReasonID: any; Reason: string }[]>([]);
        const [selectedAppointmentReasons, setSelectedAppointmentReasons] = useState<{ ReasonID?: any; Reason: string, isCustom?: boolean }[]>([]);
        const [currentPage, setCurrentPage] = useState(1);
        const [idToDelete, setIdToDelete] = useState<string | null>(null);
        const [showAlert, setShowAlert] = useState(false);
        const [message, setMessage] = useState("");
        const [alertTitle, setAlertTitle] = useState("");
        const [isdelete, setIsdelete] = useState(false);
        const [showAddAppointmentReason, setShowAddAppointmentReason] = useState(false);
        const [searchTerm, setSearchTerm] = useState("");
        const [showAppointmentReasonDropdown, setShowAppointmentReasonDropdown] = useState(false);
        const dropdownRef = useRef<HTMLDivElement>(null);
        const [customReason, setCustomReason] = useState("");
        const [customReasonError, setCustomReasonError] = useState("");
        const [activeReasonType, setActiveReasonType] = useState<ReasonType>('missing');
    
        const isReasonExists = (reason: string) => {
            const normalized = reason.trim().toLowerCase();
        
            return (
                appointmentReasons.some((r: { Reason: string }) => r.Reason.toLowerCase() === normalized) ||
                AppointmentMissingReasons.some((r: AppointmentMissingReason) => r.Reason.toLowerCase() === normalized) ||
                selectedAppointmentReasons.some((r: { Reason: string }) => r.Reason.toLowerCase() === normalized)
            );
        };
        
        const handleAddCustomReason = () => {
            const trimmedReason = customReason.trim();
        
            if (!trimmedReason) {
                setCustomReasonError("Reason is required");
                return;
            }
        
            if (isReasonExists(trimmedReason)) {
                setCustomReasonError("This appointment reason already exists");
                return;
            }
        
            const newCustomReason = {
                Reason: trimmedReason,
                isCustom: true,
            };
        
            setSelectedAppointmentReasons(prev => [...prev, newCustomReason]);
            setCustomReason("");
            setCustomReasonError("");
        };
    
        let limit: number | undefined;
        if (location.pathname === "/location/dashboard") {
            limit = 3;
        }
        const pageSize = 10;
    
        const paginatedData = AppointmentMissingReasons?.slice(
            (currentPage - 1) * pageSize,
            currentPage * pageSize
        );
    
        const totalPages = Math.ceil((AppointmentMissingReasons?.length || 0) / pageSize);
    
        // Filter appointment reasons for dropdown (exclude already selected)
        const filteredAppointmentReasons = appointmentReasons
            .filter(ar =>
                ar.Reason.toLowerCase().includes(searchTerm.toLowerCase())
            )
            .filter(ar =>
                !AppointmentMissingReasons.some((lar: AppointmentMissingReason) => lar.ReasonID === ar.ReasonID)
            );
    
        useEffect(() => {
            setCurrentPage(1);
        }, [AppointmentMissingReasons]);
    
        useEffect(() => {
            const fetchAllAppointmentReasons = async () => {
                try {
                    const response = await LOCATION_API.FETCH_APPINTMENT_MISSING_REASONS();
                    console.log("missing====", response);
                    setAppointmentReasons(response.data?.reasons);
                } catch (error) {
                    console.error("Error fetching appointment reasons:", error);
                }
            };
            fetchAllAppointmentReasons();
        }, [AppointmentMissingReasons, PracticeLocationInfo]);
    
        // Handle click outside for dropdown
        useEffect(() => {
            const handleClickOutside = (event: MouseEvent) => {
                if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                    setShowAppointmentReasonDropdown(false);
                }
            };
            document.addEventListener("mousedown", handleClickOutside);
            return () => document.removeEventListener("mousedown", handleClickOutside);
        }, []);
    
        const confirmDelete = (id: string) => {
            setIdToDelete(id);
            setIsdelete(true);
            setAlertTitle("Confirm Delete");
            setMessage("Are you sure you want to remove this appointment reason?");
            setShowAlert(true);
        };
    
        const handleConfirmDelete = async () => {
            try {
                if (idToDelete === null) return;
                const response = await LOCATION_API.REMOVE_LOCATION_APPOINTMENT_REASON(idToDelete);
                if (response.status === 200) {
                    dispatch(RemoveAppointmentMissingReason(response.data.deletedId));
                    setIdToDelete("");
                    setAlertTitle("Success");
                    setMessage("Missing reason removed Successfully....");
                    setIsdelete(false);
                    setShowAlert(true);
                }
            } catch (error) {
                console.error("Error removing appointment reason:", error);
                setAlertTitle("Error");
                setMessage("An Unexpected Error Occurred. Please Try Later");
                setIdToDelete("");
                setIsdelete(false);
                setShowAlert(true);
            }
        };
    
        const addNewClicked = (type: ReasonType) => {
            setActiveReasonType(type);
            setShowAddAppointmentReason(true);
        };
    
        const closeAlert = () => {
            setShowAlert(false);
            setIsdelete(false);
        };
    
        const handleViewAllAppointmentReasons = () => {
            navigate("/location/appointments/appointment-missing-reasons");
        };
    
        const handleAppointmentReasonSelect = (appointmentReason: { ReasonID: any; Reason: string }) => {
            if (!selectedAppointmentReasons.some(ar => ar.ReasonID === appointmentReason.ReasonID)) {
                setSelectedAppointmentReasons([...selectedAppointmentReasons, appointmentReason]);
            }
            setShowAppointmentReasonDropdown(false);
            setSearchTerm("");
        };
    
        const removeSelectedAppointmentReason = (reasonID: any) => {
            setSelectedAppointmentReasons(selectedAppointmentReasons.filter(ar => ar.ReasonID !== reasonID));
        };
    
        const saveAppointmentReasonsToBackend = async () => {
            const dataToSend = {
                selectedAppointmentReasons,
                PracticeLocationId: PracticeLocationInfo?.PracticeLocationId
            };
            console.log("dataToSend", dataToSend);
    
            try {
                const response = await LOCATION_API.ADD_LOCATION_APPOINTMENT_REASON(dataToSend);
                if (response.status === 201) {
                    setAlertTitle("Success");
                    setMessage("Appointment Reasons added successfully!");
                    setShowAddAppointmentReason(false);
                    setSelectedAppointmentReasons([]);
                    setIsdelete(false);
                    setShowAlert(true);
                    const newAppointmentReasons = response.data.LocationAppointmentReasons;
                    console.log(newAppointmentReasons, "newAppointmentReasons");
    
                    newAppointmentReasons.forEach((appointmentReason: any) => {
                        dispatch(AddNewAppointmentMissingReason(appointmentReason));
                    });
                }
            } catch (error) {
                console.error("Error adding appointment reasons:", error);
                setAlertTitle("Error");
                setMessage("Failed to add appointment reasons. Please try again.");
                setIsdelete(false);
                setShowAlert(true);
            }
        };
    
        function formatUSDate(utcString: any, type: 'date' | 'time' = 'date') {
            const date = new Date(utcString);
            if (type === 'date') {
                return date.toLocaleString("en-US", {
                    timeZone: "America/New_York",
                    year: "numeric",
                    month: "2-digit",
                    day: "2-digit",
                });
            } else {
                return date.toLocaleString("en-US", {
                    timeZone: "America/New_York",
                    hour: "2-digit",
                    minute: "2-digit",
                    second: "2-digit",
                });
            }
        }
    
        // Function to truncate text and add ellipsis
        const truncateText = (text: string, maxLength: number = 10) => {
            if (text.length <= maxLength) return text;
            return text.slice(0, maxLength) + "...";
        };
    
        // Reusable section component
        const ReasonSection = ({ type }: { type: ReasonType }) => {
            const title = type === 'missing' 
                ? 'Location Appointment Missing Reasons' 
                : 'Location Appointment Cancel Reasons';
            const buttonText = type === 'missing'
                ? 'Add New Appointment Missing Reason'
                : 'Add New Appointment Cancel Reason';
    
            return (
                <>
                    {/* Header Section */}
                    <div className="flex items-center gap-5 text-main">
                        <AppointmentsIcon />
                        <h3 className="text-main text-2xl font-bold">{title}</h3>
                    </div>
    
                    {(totalPages > 1 && !limit) && (
                        <div className="pt-4 flex justify-between items-center">
                            <span></span>
                            <SectionPagination
                                currentPage={currentPage}
                                totalPages={totalPages}
                                totalCount={paginatedData?.length || 0}
                                pageSize={pageSize}
                                onPageChange={(page) => setCurrentPage(page)}
                            />
                        </div>
                    )}
    
                    <div className="overflow-x-auto w-full">
                        <div className="min-w-[799px] md:min-w-[800px] lg:min-w-[900px] xl:min-w-[1000px] w-full">
                            <div className="py-4 px-6 rounded grid" style={{ gridTemplateColumns: `repeat(${columns.length + (rowActions.length > 0 ? 1 : 0)}, 1fr)`, backgroundColor: bgColor, color: "white" }}>
                                {columns.map((col) => (
                                    <div key={col.key.toString()} className="px-3 font-semibold text-sm md:text-base">
                                        {col.label}
                                    </div>
                                ))}
                                {rowActions.length > 0 && <div className="px-3 text-center">Actions</div>}
                            </div>
    
                            {paginatedData && paginatedData?.length > 0 ? (
                                (limit ? paginatedData.slice(0, limit) : paginatedData).map((item: AppointmentMissingReason, index: any) => (
                                    <div key={index} className="bg-gray-100 text-gray-800 py-4 px-6 grid items-center rounded mt-2 hover:bg-gray-200" style={{ gridTemplateColumns: `repeat(${columns.length + (rowActions.length > 0 ? 1 : 0)}, 1fr)` }}>
                                        <div className="px-3 text-sm md:text-base font-semibold relative group">
                                            <span>{truncateText(String((currentPage - 1) * pageSize + index + 1))}</span>
                                            {String((currentPage - 1) * pageSize + index + 1).length > 10 && (
                                                <div className="absolute hidden group-hover:block bg-gray-800 text-white text-sm rounded py-2 px-4 z-10 -top-10 left-1/2 transform -translate-x-1/2 min-w-[150px] whitespace-nowrap">
                                                    {(currentPage - 1) * pageSize + index + 1}
                                                </div>
                                            )}
                                        </div>
                                        <div className="px-3 text-sm md:text-base font-semibold relative group">
                                            <span>{truncateText(formatUSDate(item?.updatedAt, 'date') || "-")}</span>
                                            {(formatUSDate(item?.updatedAt, 'date') || "-").length > 10 && (
                                                <div className="absolute hidden group-hover:block bg-gray-800 text-white text-sm rounded py-2 px-4 z-10 -top-10 left-1/2 transform -translate-x-1/2 min-w-[150px] whitespace-nowrap">
                                                    {formatUSDate(item?.updatedAt, 'date') || "-"}
                                                </div>
                                            )}
                                        </div>
                                        <div className="px-3 text-sm md:text-base font-semibold relative group">
                                            <span>{truncateText(formatUSDate(item?.updatedAt, 'time') || "-")}</span>
                                            {(formatUSDate(item?.updatedAt, 'time') || "-").length > 10 && (
                                                <div className="absolute hidden group-hover:block bg-gray-800 text-white text-sm rounded py-2 px-4 z-10 -top-10 left-1/2 transform -translate-x-1/2 min-w-[150px] whitespace-nowrap">
                                                    {formatUSDate(item?.updatedAt, 'time') || "-"}
                                                </div>
                                            )}
                                        </div>
                                        <div className="px-3 text-sm md:text-base font-semibold relative group">
                                            <span>{truncateText(item.Reason || "-")}</span>
                                            {(item.Reason || "-").length > 10 && (
                                                <div className="absolute hidden group-hover:block bg-gray-800 text-white text-sm rounded py-2 px-4 z-10 -top-10 left-1/2 transform -translate-x-1/2 min-w-[150px] whitespace-nowrap">
                                                    {item.Reason || "-"}
                                                </div>
                                            )}
                                        </div>
                                        <div className="px-3 flex justify-center space-x-2">
                                            <button
                                                onClick={() => confirmDelete(item.LocationReasonTypeId)}
                                                className="bg-red-600 hover:bg-red-700 text-white md:text-base text-sm px-3 
                                                font-semibold md:px-5 py-1 rounded-md transition-colors duration-200 cursor-pointer"
                                            >
                                                Remove
                                            </button>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <div className="bg-gray-100 text-gray-800 py-8 px-6 text-center rounded mt-2">
                                    <p className="text-gray-500 text-sm md:text-base">You Haven't Added Any Appointment Reasons Yet</p>
                                </div>
                            )}
                        </div>
                    </div>
    
                    {showAddAppointmentReason && activeReasonType === type && (
                        <div className="bg-gray-100 p-6 rounded-lg mt-4 h-70">
                            <h4 className="text-lg text-main font-semibold mb-4">Add New Appointment Reason</h4>
                            <div className="flex gap-6">
                                <div className="w-1/2 relative " ref={dropdownRef}>
                                    <input
                                        type="text"
                                        placeholder="Search appointment reasons..."
                                        value={searchTerm}
                                        onChange={(e) => {
                                            setSearchTerm(e.target.value);
                                            setShowAppointmentReasonDropdown(true);
                                        }}
                                        onFocus={() => setShowAppointmentReasonDropdown(true)}
                                        className="w-full p-2 mb-2 border border-gray-300 rounded "
                                    />
                                    <div className="absolute right-2 top-1/2 transform -translate-y-1/2 pointer-events-none">
                                        <ChevronDown className="w-4 h-4 text-gray-400 " />
                                    </div>
                                    {showAppointmentReasonDropdown && (
                                        <div className="max-h-32 overflow-y-auto border border-gray-300 rounded bg-white absolute z-10 w-full shadow-lg">
                                            {filteredAppointmentReasons.length > 0 ? (
                                                filteredAppointmentReasons.map((appointmentReason) => (
                                                    <div
                                                        key={appointmentReason.ReasonID}
                                                        onClick={() => handleAppointmentReasonSelect(appointmentReason)}
                                                        className="p-2 cursor-pointer hover:bg-gray-200"
                                                    >
                                                        {appointmentReason.Reason}
                                                    </div>
                                                ))
                                            ) : (
                                                <div className="p-2 text-gray-500">No appointment reasons found</div>
                                            )}
                                        </div>
                                    )}
                                </div>
    
                                <div className="w-1/2 space-y-1">
                                    <label className="block text-sm font-medium text-main mb-2">Selected Appointment Reasons</label>
                                    <div className="flex flex-wrap gap-2">
                                        {selectedAppointmentReasons.length > 0 ? (
                                            selectedAppointmentReasons.map((appointmentReason) => (
                                                <span
                                                    key={appointmentReason.ReasonID}
                                                    className="inline-flex items-center px-3 py-1 bg-gray-100 border border-gray-300 rounded-full text-sm font-bold text-gray-700"
                                                >
                                                    {appointmentReason.Reason}
                                                    <button
                                                        onClick={() => removeSelectedAppointmentReason(appointmentReason.ReasonID)}
                                                        className="ml-2 text-gray-500 hover:text-red-500 cursor-pointer"
                                                    >
                                                        <X className="w-4 h-4" />
                                                    </button>
                                                </span>
                                            ))
                                        ) : (
                                            <p className="text-sm text-gray-500">No appointment reasons selected</p>
                                        )}
                                    </div>
                                </div>
                            </div>
                            <div className="mt-4 w-1/2">
                                <label className="block text-sm font-medium text-main mb-1">
                                    Not in the list?
                                </label>
    
                                <div className="flex gap-2">
                                    <input
                                        type="text"
                                        value={customReason}
                                        onChange={(e) => {
                                            setCustomReason(e.target.value);
                                            setCustomReasonError("");
                                        }}
                                        placeholder="Enter custom appointment reason"
                                        className={`w-full p-2 border rounded ${customReasonError ? "border-red-500" : "border-gray-300"
                                            }`}
                                    />
    
                                    <button
                                        type="button"
                                        onClick={handleAddCustomReason}
                                        className="bg-main text-white px-4 rounded hover:opacity-90"
                                    >
                                        Add
                                    </button>
                                </div>
    
                                {customReasonError && (
                                    <p className="text-red-500 text-sm mt-1">{customReasonError}</p>
                                )}
                            </div>
    
                            <div className="flex justify-end mt-4 space-x-4">
                                <button
                                    onClick={() => {
                                        setShowAddAppointmentReason(false);
                                        setCustomReason("");
                                        setCustomReasonError("");
                                    }}
                                    className="border border-gray-500 text-xs sm:text-lg  px-3 py-1 sm:px-4 sm:py-1 rounded-lg cursor-pointer"
                                >
                                    Cancel
                                </button>
                                <button
                                    onClick={saveAppointmentReasonsToBackend}
                                    disabled={selectedAppointmentReasons.length === 0}
                                    className={`text-xs sm:text-lg px-3 py-1 sm:px-4 sm:py-1 cursor-pointer rounded-lg ${selectedAppointmentReasons.length === 0
                                        ? "bg-gray-300 cursor-not-allowed"
                                        : "bg-main text-white"
                                        }`}
                                    onMouseEnter={(e) => {
                                        if (selectedAppointmentReasons.length > 0) {
                                            e.currentTarget.style.backgroundColor = appSecondaryClr;
                                        }
                                    }}
                                    onMouseLeave={(e) => {
                                        if (selectedAppointmentReasons.length > 0) {
                                            e.currentTarget.style.backgroundColor = bgColor;
                                        }
                                    }}
                                >
                                    Save Appointment Reasons
                                </button>
                            </div>
                        </div>
                    )}
    
                    {(totalPages > 1 && !limit) && (
                        <div className="pt-4 flex justify-between items-center">
                            <span></span>
                            <SectionPagination
                                currentPage={currentPage}
                                totalPages={totalPages}
                                totalCount={paginatedData?.length || 0}
                                pageSize={pageSize}
                                onPageChange={(page) => setCurrentPage(page)}
                            />
                        </div>
                    )}
    
                    <div className="flex justify-center space-x-4">
                        {(limit && paginatedData.length > 3) && (
                            <button
                                onClick={handleViewAllAppointmentReasons}
                                className="border border-gray-500 hover:text-white cursor-pointer text-xs sm:text-lg px-3 py-1 sm:px-4 sm:py-1 rounded-lg"
                                onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = bgColor)}
                                onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '')}
                            >
                                View All
                            </button>
                        )}
                        {!showAddAppointmentReason && (
                            <button
                                onClick={() => addNewClicked(type)}
                                className="border border-gray-500 cursor-pointer hover:text-white text-xs sm:text-lg px-3 py-1 sm:px-4 sm:py-1 rounded-lg"
                                onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = bgColor)}
                                onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '')}
                            >
                                {buttonText}
                            </button>
                        )}
                    </div>
                </>
            );
        };
    
        return (
            <div className="pt-3 space-y-5">
                <div className="w-full">
                    <div className="bg-white rounded-2xl p-8 space-y-6">
                        <AlertModal
                            isOpen={showAlert}
                            onClose={closeAlert}
                            onConfirm={handleConfirmDelete}
                            isDeleting={isdelete}
                            title={alertTitle}
                            message={message}
                            onlyOkIsNeeded={!isdelete}
                        />
    
                        {/* Missing Reasons Section */}
                        <ReasonSection type="missing" />
                    </div>
                </div>
    
                <div className="w-full">
                    <div className="bg-white rounded-2xl p-8 space-y-6">
                        {/* Cancel Reasons Section */}
                        <ReasonSection type="cancel" />
                    </div>
                </div>
            </div>
        );
    };
    
    export default AppointmentMissingReasonSection;
