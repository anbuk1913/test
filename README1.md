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
    
        // Missing Reasons State
        const [appointmentReasons, setAppointmentReasons] = useState<{ ReasonID: any; Reason: string }[]>([]);
        const [selectedAppointmentReasons, setSelectedAppointmentReasons] = useState<{ ReasonID?: any; Reason: string, isCustom?: boolean }[]>([]);
        const [currentPage, setCurrentPage] = useState(1);
        const [showAddAppointmentReason, setShowAddAppointmentReason] = useState(false);
        const [searchTerm, setSearchTerm] = useState("");
        const [showAppointmentReasonDropdown, setShowAppointmentReasonDropdown] = useState(false);
        const dropdownRef = useRef<HTMLDivElement>(null);
        const [customReason, setCustomReason] = useState("");
        const [customReasonError, setCustomReasonError] = useState("");
    
        // Cancel Reasons State
        const [cancelReasons, setCancelReasons] = useState<{ CancelID: any; CancelReason: string }[]>([]);
        const [selectedCancelReasons, setSelectedCancelReasons] = useState<{ CancelID?: any; CancelReason: string, isCustom?: boolean }[]>([]);
        const [currentCancelPage, setCurrentCancelPage] = useState(1);
        const [showAddCancelReason, setShowAddCancelReason] = useState(false);
        const [cancelSearchTerm, setCancelSearchTerm] = useState("");
        const [showCancelReasonDropdown, setShowCancelReasonDropdown] = useState(false);
        const cancelDropdownRef = useRef<HTMLDivElement>(null);
        const [customCancelReason, setCustomCancelReason] = useState("");
        const [customCancelReasonError, setCustomCancelReasonError] = useState("");
        const [locationCancelReasons, setLocationCancelReasons] = useState<any[]>([]);
    
        // Alert State
        const [idToDelete, setIdToDelete] = useState<string | null>(null);
        const [showAlert, setShowAlert] = useState(false);
        const [message, setMessage] = useState("");
        const [alertTitle, setAlertTitle] = useState("");
        const [isdelete, setIsdelete] = useState(false);
        const [deleteType, setDeleteType] = useState<'missing' | 'cancel'>('missing');
    
        let limit: number | undefined;
        if (location.pathname === "/location/dashboard") {
            limit = 3;
        }
        const pageSize = 10;
    
        // Missing Reasons Pagination
        const paginatedData = AppointmentMissingReasons?.slice(
            (currentPage - 1) * pageSize,
            currentPage * pageSize
        );
        const totalPages = Math.ceil((AppointmentMissingReasons?.length || 0) / pageSize);
    
        // Cancel Reasons Pagination
        const paginatedCancelData = locationCancelReasons?.slice(
            (currentCancelPage - 1) * pageSize,
            currentCancelPage * pageSize
        );
        const totalCancelPages = Math.ceil((locationCancelReasons?.length || 0) / pageSize);
    
        // ==================== MISSING REASONS FUNCTIONS ====================
    
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
    
        const filteredAppointmentReasons = appointmentReasons
            .filter(ar => ar.Reason.toLowerCase().includes(searchTerm.toLowerCase()))
            .filter(ar => !AppointmentMissingReasons.some((lar: AppointmentMissingReason) => lar.ReasonID === ar.ReasonID));
    
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
    
        // ==================== CANCEL REASONS FUNCTIONS ====================
    
        const isCancelReasonExists = (reason: string) => {
            const normalized = reason.trim().toLowerCase();
            return (
                cancelReasons.some((r: { CancelReason: string }) => r.CancelReason.toLowerCase() === normalized) ||
                locationCancelReasons.some((r: any) => r.CancelReason?.toLowerCase() === normalized) ||
                selectedCancelReasons.some((r: { CancelReason: string }) => r.CancelReason.toLowerCase() === normalized)
            );
        };
    
        const handleAddCustomCancelReason = () => {
            const trimmedReason = customCancelReason.trim();
            if (!trimmedReason) {
                setCustomCancelReasonError("Reason is required");
                return;
            }
            if (isCancelReasonExists(trimmedReason)) {
                setCustomCancelReasonError("This cancel reason already exists");
                return;
            }
            const newCustomReason = {
                CancelReason: trimmedReason,
                isCustom: true,
            };
            setSelectedCancelReasons(prev => [...prev, newCustomReason]);
            setCustomCancelReason("");
            setCustomCancelReasonError("");
        };
    
        const filteredCancelReasons = cancelReasons
            .filter(cr => cr.CancelReason.toLowerCase().includes(cancelSearchTerm.toLowerCase()))
            .filter(cr => !locationCancelReasons.some((lcr: any) => lcr.CancelID === cr.CancelID));
    
        const handleCancelReasonSelect = (cancelReason: { CancelID: any; CancelReason: string }) => {
            if (!selectedCancelReasons.some(cr => cr.CancelID === cancelReason.CancelID)) {
                setSelectedCancelReasons([...selectedCancelReasons, cancelReason]);
            }
            setShowCancelReasonDropdown(false);
            setCancelSearchTerm("");
        };
    
        const removeSelectedCancelReason = (cancelID: any) => {
            setSelectedCancelReasons(selectedCancelReasons.filter(cr => cr.CancelID !== cancelID));
        };
    
        const saveCancelReasonsToBackend = async () => {
            const dataToSend = {
                selectedCancelReasons,
                PracticeLocationId: PracticeLocationInfo?.PracticeLocationId
            };
            console.log("Cancel dataToSend", dataToSend);
    
            try {
                const response = await LOCATION_API.ADD_LOCATION_CANCEL_REASON(dataToSend);
                if (response.status === 201) {
                    setAlertTitle("Success");
                    setMessage("Cancel Reasons added successfully!");
                    setShowAddCancelReason(false);
                    setSelectedCancelReasons([]);
                    setIsdelete(false);
                    setShowAlert(true);
                    // Refresh cancel reasons
                    fetchLocationCancelReasons();
                }
            } catch (error) {
                console.error("Error adding cancel reasons:", error);
                setAlertTitle("Error");
                setMessage("Failed to add cancel reasons. Please try again.");
                setIsdelete(false);
                setShowAlert(true);
            }
        };
    
        const fetchLocationCancelReasons = async () => {
            try {
                const response = await LOCATION_API.FETCH_APPOINTMENT_CANCEL_REASON_BY_LOCATION(PracticeLocationInfo?.PracticeLocationId);
                if (response.status === 200) {
                    // Assuming the API returns an array of cancel reasons with CancelID, CancelReason, updatedAt
                    const reasons = Array.isArray(response.data.cancelReasons) 
                        ? response.data.cancelReasons 
                        : response.data.cancelReasons 
                            ? [response.data.cancelReasons] 
                            : [];
                    setLocationCancelReasons(reasons);
                }
            } catch (error) {
                console.log("Error fetch cancel", error);
                setLocationCancelReasons([]);
            }
        };
    
        // ==================== COMMON FUNCTIONS ====================
    
        const confirmDelete = (id: string, type: 'missing' | 'cancel' = 'missing') => {
            setIdToDelete(id);
            setDeleteType(type);
            setIsdelete(true);
            setAlertTitle("Confirm Delete");
            setMessage(`Are you sure you want to remove this ${type === 'missing' ? 'appointment' : 'cancel'} reason?`);
            setShowAlert(true);
        };
    
        const handleConfirmDelete = async () => {
            try {
                if (idToDelete === null) return;
                
                if (deleteType === 'missing') {
                    const response = await LOCATION_API.REMOVE_LOCATION_APPOINTMENT_REASON(idToDelete);
                    if (response.status === 200) {
                        dispatch(RemoveAppointmentMissingReason(response.data.deletedId));
                        setIdToDelete("");
                        setAlertTitle("Success");
                        setMessage("Missing reason removed Successfully....");
                        setIsdelete(false);
                        setShowAlert(true);
                    }
                } else {
                    const response = await LOCATION_API.REMOVE_LOCATION_CANCEL_REASON(idToDelete);
                    if (response.status === 200) {
                        setIdToDelete("");
                        setAlertTitle("Success");
                        setMessage("Cancel reason removed Successfully....");
                        setIsdelete(false);
                        setShowAlert(true);
                        // Refresh cancel reasons
                        fetchLocationCancelReasons();
                    }
                }
            } catch (error) {
                console.error("Error removing reason:", error);
                setAlertTitle("Error");
                setMessage("An Unexpected Error Occurred. Please Try Later");
                setIdToDelete("");
                setIsdelete(false);
                setShowAlert(true);
            }
        };
    
        const closeAlert = () => {
            setShowAlert(false);
            setIsdelete(false);
        };
    
        const addNewMissingReasonClicked = () => {
            setShowAddAppointmentReason(true);
        };
    
        const addNewCancelReasonClicked = () => {
            setShowAddCancelReason(true);
        };
    
        const handleViewAllAppointmentReasons = () => {
            navigate("/location/appointments/appointment-missing-reasons");
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
    
        const truncateText = (text: string, maxLength: number = 10) => {
            if (text.length <= maxLength) return text;
            return text.slice(0, maxLength) + "...";
        };
    
        // ==================== USE EFFECTS ====================
    
        useEffect(() => {
            setCurrentPage(1);
        }, [AppointmentMissingReasons]);
    
        useEffect(() => {
            setCurrentCancelPage(1);
        }, [locationCancelReasons]);
    
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
    
        useEffect(() => {
            const fetchAllCancelReasons = async () => {
                try {
                    const response = await LOCATION_API.FETCH_APPOINTMENT_CANCEL_REASONS();
                    console.log("cancel reasons====", response);
                    setCancelReasons(response.data?.cancelReasons || []);
                } catch (error) {
                    console.error("Error fetching cancel reasons:", error);
                }
            };
            fetchAllCancelReasons();
        }, [locationCancelReasons, PracticeLocationInfo]);
    
        useEffect(() => {
            fetchLocationCancelReasons();
        }, [PracticeLocationInfo]);
    
        // Handle click outside for dropdowns
        useEffect(() => {
            const handleClickOutside = (event: MouseEvent) => {
                if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                    setShowAppointmentReasonDropdown(false);
                }
                if (cancelDropdownRef.current && !cancelDropdownRef.current.contains(event.target as Node)) {
                    setShowCancelReasonDropdown(false);
                }
            };
            document.addEventListener("mousedown", handleClickOutside);
            return () => document.removeEventListener("mousedown", handleClickOutside);
        }, []);
    
        // ==================== RENDER COMPONENTS ====================
    
        const renderTableHeader = () => (
            <div className="py-4 px-6 rounded grid" style={{ gridTemplateColumns: `repeat(${columns.length + (rowActions.length > 0 ? 1 : 0)}, 1fr)`, backgroundColor: bgColor, color: "white" }}>
                {columns.map((col) => (
                    <div key={col.key.toString()} className="px-3 font-semibold text-sm md:text-base">
                        {col.label}
                    </div>
                ))}
                {rowActions.length > 0 && <div className="px-3 text-center">Actions</div>}
            </div>
        );
    
        const renderMissingReasonRow = (item: AppointmentMissingReason, index: number) => (
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
                        onClick={() => confirmDelete(item.LocationReasonTypeId, 'missing')}
                        className="bg-red-600 hover:bg-red-700 text-white md:text-base text-sm px-3 font-semibold md:px-5 py-1 rounded-md transition-colors duration-200 cursor-pointer"
                    >
                        Remove
                    </button>
                </div>
            </div>
        );
    
        const renderCancelReasonRow = (item: any, index: number) => (
            <div key={index} className="bg-gray-100 text-gray-800 py-4 px-6 grid items-center rounded mt-2 hover:bg-gray-200" style={{ gridTemplateColumns: `repeat(${columns.length + (rowActions.length > 0 ? 1 : 0)}, 1fr)` }}>
                <div className="px-3 text-sm md:text-base font-semibold relative group">
                    <span>{truncateText(String((currentCancelPage - 1) * pageSize + index + 1))}</span>
                    {String((currentCancelPage - 1) * pageSize + index + 1).length > 10 && (
                        <div className="absolute hidden group-hover:block bg-gray-800 text-white text-sm rounded py-2 px-4 z-10 -top-10 left-1/2 transform -translate-x-1/2 min-w-[150px] whitespace-nowrap">
                            {(currentCancelPage - 1) * pageSize + index + 1}
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
                    <span>{truncateText(item.CancelReason || "-")}</span>
                    {(item.CancelReason || "-").length > 10 && (
                        <div className="absolute hidden group-hover:block bg-gray-800 text-white text-sm rounded py-2 px-4 z-10 -top-10 left-1/2 transform -translate-x-1/2 min-w-[150px] whitespace-nowrap">
                            {item.CancelReason || "-"}
                        </div>
                    )}
                </div>
                <div className="px-3 flex justify-center space-x-2">
                    <button
                        onClick={() => confirmDelete(item.CancelID, 'cancel')}
                        className="bg-red-600 hover:bg-red-700 text-white md:text-base text-sm px-3 font-semibold md:px-5 py-1 rounded-md transition-colors duration-200 cursor-pointer"
                    >
                        Remove
                    </button>
                </div>
            </div>
        );
    
        const renderAddReasonForm = (
            type: 'missing' | 'cancel',
            searchValue: string,
            setSearchValue: (value: string) => void,
            showDropdown: boolean,
            setShowDropdown: (show: boolean) => void,
            filteredReasons: any[],
            handleReasonSelect: (reason: any) => void,
            selectedReasons: any[],
            removeSelectedReason: (id: any) => void,
            customReasonValue: string,
            setCustomReasonValue: (value: string) => void,
            customReasonErrorValue: string,
            setCustomReasonErrorValue: (value: string) => void,
            handleAddCustom: () => void,
            saveReasons: () => void,
            setShowAdd: (show: boolean) => void,
            dropdownRefProp: React.RefObject<HTMLDivElement>
        ) => (
            <div className="bg-gray-100 p-6 rounded-lg mt-4 h-70">
                <h4 className="text-lg text-main font-semibold mb-4">
                    Add New {type === 'missing' ? 'Appointment Missing' : 'Appointment Cancel'} Reason
                </h4>
                <div className="flex gap-6">
                    <div className="w-1/2 relative" ref={dropdownRefProp}>
                        <input
                            type="text"
                            placeholder={`Search ${type === 'missing' ? 'appointment' : 'cancel'} reasons...`}
                            value={searchValue}
                            onChange={(e) => {
                                setSearchValue(e.target.value);
                                setShowDropdown(true);
                            }}
                            onFocus={() => setShowDropdown(true)}
                            className="w-full p-2 mb-2 border border-gray-300 rounded"
                        />
                        <div className="absolute right-2 top-1/2 transform -translate-y-1/2 pointer-events-none">
                            <ChevronDown className="w-4 h-4 text-gray-400" />
                        </div>
                        {showDropdown && (
                            <div className="max-h-32 overflow-y-auto border border-gray-300 rounded bg-white absolute z-10 w-full shadow-lg">
                                {filteredReasons.length > 0 ? (
                                    filteredReasons.map((reason) => (
                                        <div
                                            key={type === 'missing' ? reason.ReasonID : reason.CancelID}
                                            onClick={() => handleReasonSelect(reason)}
                                            className="p-2 cursor-pointer hover:bg-gray-200"
                                        >
                                            {type === 'missing' ? reason.Reason : reason.CancelReason}
                                        </div>
                                    ))
                                ) : (
                                    <div className="p-2 text-gray-500">No {type === 'missing' ? 'appointment' : 'cancel'} reasons found</div>
                                )}
                            </div>
                        )}
                    </div>
    
                    <div className="w-1/2 space-y-1">
                        <label className="block text-sm font-medium text-main mb-2">
                            Selected {type === 'missing' ? 'Appointment' : 'Cancel'} Reasons
                        </label>
                        <div className="flex flex-wrap gap-2">
                            {selectedReasons.length > 0 ? (
                                selectedReasons.map((reason, idx) => (
                                    <span
                                        key={type === 'missing' ? reason.ReasonID || idx : reason.CancelID || idx}
                                        className="inline-flex items-center px-3 py-1 bg-gray-100 border border-gray-300 rounded-full text-sm font-bold text-gray-700"
                                    >
                                        {type === 'missing' ? reason.Reason : reason.CancelReason}
                                        <button
                                            onClick={() => removeSelectedReason(type === 'missing' ? reason.ReasonID : reason.CancelID)}
                                            className="ml-2 text-gray-500 hover:text-red-500 cursor-pointer"
                                        >
                                            <X className="w-4 h-4" />
                                        </button>
                                    </span>
                                ))
                            ) : (
                                <p className="text-sm text-gray-500">No {type === 'missing' ? 'appointment' : 'cancel'} reasons selected</p>
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
                            value={customReasonValue}
                            onChange={(e) => {
                                setCustomReasonValue(e.target.value);
                                setCustomReasonErrorValue("");
                            }}
                            placeholder={`Enter custom ${type === 'missing' ? 'appointment' : 'cancel'} reason`}
                            className={`w-full p-2 border rounded ${customReasonErrorValue ? "border-red-500" : "border-gray-300"}`}
                        />
                        <button
                            type="button"
                            onClick={handleAddCustom}
                            className="bg-main text-white px-4 rounded hover:opacity-90"
                        >
                            Add
                        </button>
                    </div>
                    {customReasonErrorValue && (
                        <p className="text-red-500 text-sm mt-1">{customReasonErrorValue}</p>
                    )}
                </div>
    
                <div className="flex justify-end mt-4 space-x-4">
                    <button
                        onClick={() => {
                            setShowAdd(false);
                            setCustomReasonValue("");
                            setCustomReasonErrorValue("");
                        }}
                        className="border border-gray-500 text-xs sm:text-lg px-3 py-1 sm:px-4 sm:py-1 rounded-lg cursor-pointer"
                    >
                        Cancel
                    </button>
                    <button
                        onClick={saveReasons}
                        disabled={selectedReasons.length === 0}
                        className={`text-xs sm:text-lg px-3 py-1 sm:px-4 sm:py-1 cursor-pointer rounded-lg ${
                            selectedReasons.length === 0 ? "bg-gray-300 cursor-not-allowed" : "bg-main text-white"
                        }`}
                        onMouseEnter={(e) => {
                            if (selectedReasons.length > 0) {
                                e.currentTarget.style.backgroundColor = appSecondaryClr;
                            }
                        }}
                        onMouseLeave={(e) => {
                            if (selectedReasons.length > 0) {
                                e.currentTarget.style.backgroundColor = bgColor;
                            }
                        }}
                    >
                        Save {type === 'missing' ? 'Appointment' : 'Cancel'} Reasons
                    </button>
                </div>
            </div>
        );
    
        return (
            <div className="pt-3 space-y-5">
                {/* MISSING REASONS SECTION */}
                <div className="w-full">
                    <div className="bg-white rounded-2xl p-8 space-y-6">
                        <div className="flex items-center gap-5 text-main">
                            <AppointmentsIcon />
                            <h3 className="text-main text-2xl font-bold">Location Appointment Missing Reasons</h3>
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
    
                        <AlertModal
                            isOpen={showAlert}
                            onClose={closeAlert}
                            onConfirm={handleConfirmDelete}
                            isDeleting={isdelete}
                            title={alertTitle}
                            message={message}
                            onlyOkIsNeeded={!isdelete}
                        />
    
                        <div className="overflow-x-auto w-full">
                            <div className="min-w-[799px] md:min-w-[800px] lg:min-w-[900px] xl:min-w-[1000px] w-full">
                                {renderTableHeader()}
    
                                {paginatedData && paginatedData?.length > 0 ? (
                                    (limit ? paginatedData.slice(0, limit) : paginatedData).map((item: AppointmentMissingReason, index: any) =>
                                        renderMissingReasonRow(item, index)
                                    )
                                ) : (
                                    <div className="bg-gray-100 text-gray-800 py-8 px-6 text-center rounded mt-2">
                                        <p className="text-gray-500 text-sm md:text-base">You Haven't Added Any Appointment Missing Reasons Yet</p>
                                    </div>
                                )}
                            </div>
                        </div>
    
                        {showAddAppointmentReason && renderAddReasonForm(
                            'missing',
                            searchTerm,
                            setSearchTerm,
                            showAppointmentReasonDropdown,
                            setShowAppointmentReasonDropdown,
                            filteredAppointmentReasons,
                            handleAppointmentReasonSelect,
                            selectedAppointmentReasons,
                            removeSelectedAppointmentReason,
                            customReason,
                            setCustomReason,
                            customReasonError,
                            setCustomReasonError,
                            handleAddCustomReason,
                            saveAppointmentReasonsToBackend,
                            setShowAddAppointmentReason,
                            dropdownRef
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
                                    onClick={addNewMissingReasonClicked}
                                    className="border border-gray-500 cursor-pointer hover:text-white text-xs sm:text-lg px-3 py-1 sm:px-4 sm:py-1 rounded-lg"
                                    onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = bgColor)}
                                    onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '')}
                                >
                                    Add New Appointment Missing Reason
                                </button>
                            )}
                        </div>
                    </div>
                </div>
    
                {/* CANCEL REASONS SECTION */}
                <div className="w-full">
                    <div className="bg-white rounded-2xl p-8 space-y-6">
                        <div className="flex items-center gap-5 text-main">
                            <AppointmentsIcon />
                            <h3 className="text-main text-2xl font-bold">Location Appointment Cancel Reasons</h3>
                        </div>
    
                        {(totalCancelPages > 1 && !limit) && (
                            <div className="pt-4 flex justify-between items-center">
                                <span></span>
                                <SectionPagination
                                    currentPage={currentCancelPage}
                                    totalPages={totalCancelPages}
                                    totalCount={paginatedCancelData?.length || 0}
                                    pageSize={pageSize}
                                    onPageChange={(page) => setCurrentCancelPage(page)}
                                />
                            </div>
                        )}
    
                        <div className="overflow-x-auto w-full">
                            <div className="min-w-[799px] md:min-w-[800px] lg:min-w-[900px] xl:min-w-[1000px] w-full">
                                {renderTableHeader()}
    
                                {locationCancelReasons && locationCancelReasons.length > 0 ? (
                                    (limit ? paginatedCancelData.slice(0, limit) : paginatedCancelData).map((item: any, index: number) =>
                                        renderCancelReasonRow(item, index)
                                    )
                                ) : (
                                    <div className="bg-gray-100 text-gray-800 py-8 px-6 text-center rounded mt-2">
                                        <p className="text-gray-500 text-sm md:text-base">You Haven't Added Any Appointment Cancel Reasons Yet</p>
                                    </div>
                                )}
                            </div>
                        </div>
    
                        {showAddCancelReason && renderAddReasonForm(
                            'cancel',
                            cancelSearchTerm,
                            setCancelSearchTerm,
                            showCancelReasonDropdown,
                            setShowCancelReasonDropdown,
                            filteredCancelReasons,
                            handleCancelReasonSelect,
                            selectedCancelReasons,
                            removeSelectedCancelReason,
                            customCancelReason,
                            setCustomCancelReason,
                            customCancelReasonError,
                            setCustomCancelReasonError,
                            handleAddCustomCancelReason,
                            saveCancelReasonsToBackend,
                            setShowAddCancelReason,
                            cancelDropdownRef
                        )}
    
                        {(totalCancelPages > 1 && !limit) && (
                            <div className="pt-4 flex justify-between items-center">
                                <span></span>
                                <SectionPagination
                                    currentPage={currentCancelPage}
                                    totalPages={totalCancelPages}
                                    totalCount={paginatedCancelData?.length || 0}
                                    pageSize={pageSize}
                                    onPageChange={(page) => setCurrentCancelPage(page)}
                                />
                            </div>
                        )}
    
                        <div className="flex justify-center space-x-4">
                            {!showAddCancelReason && (
                                <button
                                    onClick={addNewCancelReasonClicked}
                                    className="border border-gray-500 cursor-pointer hover:text-white text-xs sm:text-lg px-3 py-1 sm:px-4 sm:py-1 rounded-lg"
                                    onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = bgColor)}
                                    onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '')}
                                >
                                    Add New Appointment Cancel Reason
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        );
    };
    
    export default AppointmentMissingReasonSection;
