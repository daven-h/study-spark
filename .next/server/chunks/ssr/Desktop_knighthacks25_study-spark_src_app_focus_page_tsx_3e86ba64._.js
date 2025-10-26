module.exports = [
"[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>FocusSessionPage
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/knighthacks25/study-spark/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/knighthacks25/study-spark/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/knighthacks25/study-spark/node_modules/next/navigation.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$src$2f$store$2f$app$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/knighthacks25/study-spark/src/store/app-store.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$src$2f$components$2f$ui$2f$button$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/knighthacks25/study-spark/src/components/ui/button.tsx [app-ssr] (ecmascript)");
'use client';
;
;
;
;
;
function FocusSessionPage() {
    const router = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRouter"])();
    const { addSession, lastMethod } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$src$2f$store$2f$app$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useAppStore"])();
    const [isSessionActive, setIsSessionActive] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [sessionDuration, setSessionDuration] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(0);
    const [sessionStartTime, setSessionStartTime] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [isClient, setIsClient] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [attentionData, setAttentionData] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])({
        attention_score: 0,
        eye_ar: 0,
        mouth_ar: 0,
        head_tilt: 0,
        phone_detected: false,
        fps: 0,
        timestamp: 0,
        focus_status: 'unknown',
        session_active: false
    });
    const [websocketConnected, setWebsocketConnected] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [apiConnected, setApiConnected] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const videoRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const streamRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const intervalRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const websocketRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const pollingRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    // Set client-side flag to prevent hydration issues
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        setIsClient(true);
    }, []);
    // Connect to HTTP API server
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        if (isClient) {
            connectToAPI();
        }
        return ()=>{
            disconnectFromAPI();
        };
    }, [
        isClient
    ]);
    // Start camera when component mounts
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        if (isClient) {
            startCamera();
        }
        return ()=>{
            stopCamera();
        };
    }, [
        isClient
    ]);
    const connectToAPI = async ()=>{
        try {
            const response = await fetch('http://localhost:8765/api/ping');
            if (response.ok) {
                setApiConnected(true);
                console.log('API server connected');
            } else {
                setApiConnected(false);
                console.log('API server not responding');
            }
        } catch (error) {
            console.error('Failed to connect to API:', error);
            setApiConnected(false);
        }
    };
    const disconnectFromAPI = ()=>{
        if (pollingRef.current) {
            clearInterval(pollingRef.current);
            pollingRef.current = null;
        }
        setApiConnected(false);
    };
    const sendAPICommand = async (command)=>{
        if (!apiConnected) return;
        try {
            const endpoint = command === 'start_tracking' ? 'start_tracking' : command === 'stop_tracking' ? 'stop_tracking' : 'ping';
            const response = await fetch(`http://localhost:8765/api/${endpoint}`, {
                method: endpoint === 'ping' ? 'GET' : 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (response.ok) {
                const data = await response.json();
                console.log(`API command ${command}:`, data);
                return data;
            }
        } catch (error) {
            console.error(`API command ${command} failed:`, error);
        }
    };
    const pollAttentionData = ()=>{
        if (!apiConnected) return;
        const poll = async ()=>{
            try {
                const response = await fetch('http://localhost:8765/api/attention_data', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                if (response.ok) {
                    const data = await response.json();
                    if (data.success) {
                        setAttentionData(data.data);
                    }
                } else {
                    console.error('API responded with error:', response.status);
                }
            } catch (error) {
                console.error('Failed to poll attention data:', error);
                // Don't spam the console with errors
                if (Math.random() < 0.1) {
                    console.error('Polling error:', error);
                }
            }
        };
        // Poll every 100ms (10 Hz)
        pollingRef.current = setInterval(poll, 100);
    };
    const startCamera = async ()=>{
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: {
                        ideal: 1280
                    },
                    height: {
                        ideal: 720
                    },
                    facingMode: 'user'
                }
            });
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
                streamRef.current = stream;
            }
        } catch (error) {
            console.error('Error accessing camera:', error);
        // Fallback: show a placeholder or message
        }
    };
    const stopCamera = ()=>{
        if (streamRef.current) {
            streamRef.current.getTracks().forEach((track)=>track.stop());
            streamRef.current = null;
        }
    };
    const startSession = async ()=>{
        setIsSessionActive(true);
        const startTime = Date.now();
        setSessionStartTime(startTime);
        setSessionDuration(0);
        // Start attention tracking via API
        await sendAPICommand('start_tracking');
        pollAttentionData();
        // Start timer
        intervalRef.current = setInterval(()=>{
            setSessionDuration(Math.floor((Date.now() - startTime) / 1000));
        }, 1000);
    };
    const stopSession = async ()=>{
        if (intervalRef.current) {
            clearInterval(intervalRef.current);
        }
        // Stop attention tracking via API
        await sendAPICommand('stop_tracking');
        disconnectFromAPI();
        setIsSessionActive(false);
        // Calculate session duration in minutes
        const durationMinutes = Math.floor(sessionDuration / 60);
        // Create session record with attention data
        const session = {
            id: `session-${Date.now()}`,
            title: `${lastMethod ? lastMethod.replace('-', ' ') : 'Study'} Session`,
            method: lastMethod || 'pomodoro',
            completed: true,
            minutes: durationMinutes,
            dateISO: new Date().toISOString().split('T')[0],
            createdAt: Date.now(),
            attentionScore: Math.round(attentionData.attention_score * 100),
            avgEyeAR: attentionData.eye_ar,
            avgMouthAR: attentionData.mouth_ar,
            phoneDetected: attentionData.phone_detected
        };
        addSession(session);
        // Stop camera
        stopCamera();
        // Redirect to progress page
        router.push('/progress');
    };
    const formatTime = (seconds)=>{
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    };
    // Determine if user is distracted
    // Only show popup when there's a clear distraction event, not just ambient detection
    const isDistracted = attentionData.phone_detected && attentionData.focus_status === 'distracted';
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("main", {
        className: "min-h-screen bg-[#fffbef] flex flex-col",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "bg-white border-b border-[rgba(63,64,63,0.08)] px-6 py-4",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "max-w-6xl mx-auto flex justify-between items-center",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                                    className: "text-2xl font-modular text-[#3f403f]",
                                    children: "Focus Session"
                                }, void 0, false, {
                                    fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                    lineNumber: 252,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                    className: "text-sm font-norwester text-[#575b44]",
                                    children: [
                                        lastMethod ? lastMethod.replace('-', ' ').toUpperCase() : 'STUDY',
                                        " Method"
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                    lineNumber: 255,
                                    columnNumber: 13
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                            lineNumber: 251,
                            columnNumber: 11
                        }, this),
                        isSessionActive && isClient && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "text-right",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "text-3xl font-modular text-[#939f5c]",
                                    children: formatTime(sessionDuration)
                                }, void 0, false, {
                                    fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                    lineNumber: 262,
                                    columnNumber: 15
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "text-sm font-norwester text-[#575b44]",
                                    children: "Session Time"
                                }, void 0, false, {
                                    fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                    lineNumber: 265,
                                    columnNumber: 15
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                            lineNumber: 261,
                            columnNumber: 13
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                    lineNumber: 250,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                lineNumber: 249,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex-1 flex flex-col items-center justify-center p-6",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "relative w-full max-w-4xl aspect-video bg-black rounded-2xl overflow-hidden shadow-lg",
                        children: [
                            isClient ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("video", {
                                ref: videoRef,
                                autoPlay: true,
                                playsInline: true,
                                muted: true,
                                className: "w-full h-full object-cover scale-x-[-1]"
                            }, void 0, false, {
                                fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                lineNumber: 277,
                                columnNumber: 13
                            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "w-full h-full flex items-center justify-center text-white",
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "text-center",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "text-2xl mb-2",
                                            children: "📹"
                                        }, void 0, false, {
                                            fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                            lineNumber: 287,
                                            columnNumber: 17
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "text-sm",
                                            children: "Loading Camera..."
                                        }, void 0, false, {
                                            fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                            lineNumber: 288,
                                            columnNumber: 17
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                    lineNumber: 286,
                                    columnNumber: 15
                                }, this)
                            }, void 0, false, {
                                fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                lineNumber: 285,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "absolute inset-0 pointer-events-none",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: `absolute top-4 left-4 px-3 py-1 rounded-full text-sm font-norwester ${apiConnected ? 'bg-green-500 text-white' : 'bg-red-500 text-white'}`,
                                        children: apiConnected ? '🔗 AI Connected' : '❌ AI Disconnected'
                                    }, void 0, false, {
                                        fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                        lineNumber: 296,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: `border-2 rounded-full opacity-50 ${attentionData.focus_status === 'focused' ? 'border-green-400' : attentionData.focus_status === 'distracted' ? 'border-red-400' : 'border-yellow-400'}`,
                                                style: {
                                                    width: '1260px',
                                                    height: '700px',
                                                    position: 'absolute',
                                                    left: '50%',
                                                    top: '50%',
                                                    transform: 'translate(-50%, -50%)'
                                                }
                                            }, void 0, false, {
                                                fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                                lineNumber: 305,
                                                columnNumber: 15
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: `border border-white rounded-full opacity-30 ${attentionData.focus_status === 'focused' ? 'border-green-300' : attentionData.focus_status === 'distracted' ? 'border-red-300' : 'border-yellow-300'}`,
                                                style: {
                                                    width: '1252px',
                                                    height: '692px',
                                                    position: 'absolute',
                                                    left: '50%',
                                                    top: '50%',
                                                    transform: 'translate(-50%, -50%)'
                                                }
                                            }, void 0, false, {
                                                fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                                lineNumber: 319,
                                                columnNumber: 15
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                        lineNumber: 303,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "absolute top-4 right-4 space-y-2",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: `px-2 py-1 rounded text-xs font-norwester ${attentionData.focus_status === 'focused' ? 'bg-green-500 text-white' : attentionData.focus_status === 'distracted' ? 'bg-red-500 text-white' : 'bg-yellow-500 text-white'}`,
                                                children: attentionData.focus_status === 'focused' ? '✅ Focused' : attentionData.focus_status === 'distracted' ? '❌ Distracted' : '⏳ Analyzing...'
                                            }, void 0, false, {
                                                fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                                lineNumber: 335,
                                                columnNumber: 15
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "bg-blue-500 text-white px-2 py-1 rounded text-xs font-norwester",
                                                children: [
                                                    "👁️ Eye AR: ",
                                                    attentionData.eye_ar.toFixed(2)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                                lineNumber: 345,
                                                columnNumber: 15
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "bg-purple-500 text-white px-2 py-1 rounded text-xs font-norwester",
                                                children: [
                                                    "🧠 Score: ",
                                                    Math.round(attentionData.attention_score * 100),
                                                    "%"
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                                lineNumber: 349,
                                                columnNumber: 15
                                            }, this),
                                            attentionData.phone_detected && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "bg-red-600 text-white px-2 py-1 rounded text-xs font-norwester",
                                                children: "📱 Phone Detected!"
                                            }, void 0, false, {
                                                fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                                lineNumber: 354,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "bg-gray-600 text-white px-2 py-1 rounded text-xs font-norwester",
                                                children: [
                                                    "📊 FPS: ",
                                                    Math.round(attentionData.fps)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                                lineNumber: 359,
                                                columnNumber: 15
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                        lineNumber: 334,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                lineNumber: 294,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                        lineNumber: 275,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "mt-8 text-center max-w-2xl",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                className: "text-xl font-modular text-[#3f403f] mb-4",
                                children: isSessionActive ? 'Stay Focused!' : 'Ready to Start?'
                            }, void 0, false, {
                                fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                lineNumber: 368,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "text-[#575b44] font-norwester mb-6",
                                children: isSessionActive ? 'Keep your eyes on the screen and maintain good posture. AI is tracking your focus, eye movement, and detecting distractions like phones.' : apiConnected ? 'Position yourself in front of the camera and click "Start Session" when you\'re ready to begin. AI will track your attention in real-time.' : 'AI attention tracking is not connected. Please start the Python server first.'
                            }, void 0, false, {
                                fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                                lineNumber: 371,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                        lineNumber: 367,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                lineNumber: 274,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "bg-white border-t border-[rgba(63,64,63,0.08)] px-6 py-6",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "max-w-6xl mx-auto flex justify-center",
                    children: !isSessionActive ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$src$2f$components$2f$ui$2f$button$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                        onClick: startSession,
                        disabled: !apiConnected,
                        className: `font-modular px-8 py-4 text-lg rounded-2xl shadow-lg ${apiConnected ? 'bg-[#939f5c] text-[#3f403f] hover:bg-[#808b4f]' : 'bg-gray-400 text-gray-600 cursor-not-allowed'}`,
                        children: apiConnected ? 'Start Session' : 'AI Not Connected'
                    }, void 0, false, {
                        fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                        lineNumber: 386,
                        columnNumber: 13
                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$src$2f$components$2f$ui$2f$button$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                        onClick: stopSession,
                        className: "font-modular bg-red-500 text-white hover:bg-red-600 px-8 py-4 text-lg rounded-2xl shadow-lg",
                        children: "Stop Session"
                    }, void 0, false, {
                        fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                        lineNumber: 398,
                        columnNumber: 13
                    }, this)
                }, void 0, false, {
                    fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                    lineNumber: 384,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
                lineNumber: 383,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/Desktop/knighthacks25/study-spark/src/app/focus/page.tsx",
        lineNumber: 244,
        columnNumber: 5
    }, this);
}
}),
];

//# sourceMappingURL=Desktop_knighthacks25_study-spark_src_app_focus_page_tsx_3e86ba64._.js.map