1️⃣ Create a helper for storage

    const STORAGE_KEY = 'secured_file_state';
    
    const saveState = (state: Partial<{
      stage: Stage;
      communicationType: 'sms' | 'email';
      expiryTime: number;
      token: string;
    }>) => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    };
    
    const getSavedState = () => {
      const data = localStorage.getItem(STORAGE_KEY);
      return data ? JSON.parse(data) : null;
    };
    
    const clearState = () => {
      localStorage.removeItem(STORAGE_KEY);
    };


2️⃣ Restore state on page load

Update your useEffect:


    useEffect(() => {
      const saved = getSavedState();
    
      if (saved?.stage) {
        setStage(saved.stage);
        if (saved.communicationType) setCommunicationType(saved.communicationType);
        if (saved.expiryTime) setExpiryTime(saved.expiryTime);
        if (saved.token) setToken(saved.token);
      } else {
        checkAccess();
      }
    }, [id]);


3️⃣ Save state when OTP method page is shown

    const checkAccess = async () => {
      if (!id) return;
    
      const data = await securedFilesAPI.checkAccess(id);
    
      if (!data.success) {
        setStage('not-found');
      } else {
        setEmail(maskEmail(data.email!));
        setPhone(maskPhone(data.phone!));
        setCommunicationType(data.communicationType!);
        setStage('otp-method');
    
        saveState({
          stage: 'otp-method',
          communicationType: data.communicationType
        });
      }
    };


4️⃣ Save state after OTP is sent


    const handleSendOTP = async (method: 'sms' | 'email') => {
      if (!id) return;
    
      setLoading(true);
      const data = await securedFilesAPI.sendOTP(id, method);
      setLoading(false);
    
      if (data.success) {
        setExpiryTime(data.expiryTime);
        setStage('otp-verify');
    
        saveState({
          stage: 'otp-verify',
          communicationType: method,
          expiryTime: data.expiryTime
        });
      }
    };


5️⃣ Save state after OTP verification

    const handleVerifyOTP = async (otp: string) => {
      if (!id) return;
    
      setLoading(true);
      const data = await securedFilesAPI.verifyOTP(id, otp);
      setLoading(false);
    
      if (data.success) {
        setToken(data.token);
        setStage('passkey');
    
        saveState({
          stage: 'passkey',
          token: data.token
        });
      } else {
        alert(data.message);
      }
    };


6️⃣ Clear storage after success

    const handleVerifyPasskey = async (passkey: string) => {
      if (!id) return;
    
      setLoading(true);
      const data = await securedFilesAPI.verifyPasskey(id, passkey, token);
      setLoading(false);
    
      if (data.success) {
        clearState(); // 🔥 important
        setStage('success');
        window.location.href = data.fileUrl!;
      } else {
        alert(data.message);
      }
    };


