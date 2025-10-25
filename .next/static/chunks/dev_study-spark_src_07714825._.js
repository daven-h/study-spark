(globalThis.TURBOPACK || (globalThis.TURBOPACK = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/dev/study-spark/src/types/settings.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "DEFAULT_SETTINGS",
    ()=>DEFAULT_SETTINGS
]);
const DEFAULT_SETTINGS = {
    workMin: 25,
    shortBreak: 5,
    longBreak: 15,
    cyclesToLong: 4,
    attentionThresholdSec: 30,
    yawMax: 30,
    pitchMax: 30,
    adaptiveEnabled: false,
    blockedSites: []
};
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/dev/study-spark/src/store/settingsStore.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "useSettingsStore",
    ()=>useSettingsStore
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$zustand$2f$esm$2f$react$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/node_modules/zustand/esm/react.mjs [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$zustand$2f$esm$2f$middleware$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/node_modules/zustand/esm/middleware.mjs [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$types$2f$settings$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/src/types/settings.ts [app-client] (ecmascript)");
;
;
;
const useSettingsStore = (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$zustand$2f$esm$2f$react$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["create"])()((0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$zustand$2f$esm$2f$middleware$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["persist"])((set)=>({
        ...__TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$types$2f$settings$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["DEFAULT_SETTINGS"],
        updateSettings: (updates)=>set((state)=>({
                    ...state,
                    ...updates
                })),
        resetSettings: ()=>set(__TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$types$2f$settings$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["DEFAULT_SETTINGS"])
    }), {
    name: 'settings-storage'
}));
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/dev/study-spark/src/store/sessionStore.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "useSessionStore",
    ()=>useSessionStore
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$zustand$2f$esm$2f$react$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/node_modules/zustand/esm/react.mjs [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$zustand$2f$esm$2f$middleware$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/node_modules/zustand/esm/middleware.mjs [app-client] (ecmascript)");
;
;
const useSessionStore = (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$zustand$2f$esm$2f$react$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["create"])()((0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$zustand$2f$esm$2f$middleware$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["persist"])((set, get)=>({
        sessions: [],
        currentAttentionTimeline: [],
        addSession: (sessionData)=>{
            const newSession = {
                ...sessionData,
                id: crypto.randomUUID(),
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString()
            };
            set((state)=>({
                    sessions: [
                        ...state.sessions,
                        newSession
                    ]
                }));
        },
        recordAttention: (score)=>{
            set((state)=>({
                    currentAttentionTimeline: [
                        ...state.currentAttentionTimeline,
                        score
                    ]
                }));
        },
        clearCurrentTimeline: ()=>{
            set({
                currentAttentionTimeline: []
            });
        },
        getSessionsByDate: (date)=>{
            const { sessions } = get();
            return sessions.filter((session)=>session.date.startsWith(date));
        },
        getSessionStats: (sessionId)=>{
            const { sessions } = get();
            const session = sessions.find((s)=>s.id === sessionId);
            if (!session || session.attentionTimeline.length === 0) {
                return null;
            }
            return calculateSessionStats(session);
        },
        getTodayStats: ()=>{
            const { sessions } = get();
            const today = new Date().toISOString().split('T')[0];
            const todaySessions = sessions.filter((s)=>s.date.startsWith(today));
            if (todaySessions.length === 0) {
                return {
                    totalFocusTime: 0,
                    cyclesCompleted: 0,
                    attentionScore: 0,
                    mostDistractedMinute: null
                };
            }
            // Aggregate stats from all today's sessions
            const totalFocusTime = todaySessions.reduce((sum, s)=>sum + s.workMinutes, 0);
            const cyclesCompleted = todaySessions.length;
            // Calculate average attention across all sessions
            const allScores = todaySessions.flatMap((s)=>s.attentionTimeline);
            const avgAttention = allScores.length > 0 ? allScores.reduce((sum, score)=>sum + score, 0) / allScores.length : 0;
            return {
                totalFocusTime,
                cyclesCompleted,
                attentionScore: Math.round(avgAttention * 100),
                mostDistractedMinute: null
            };
        }
    }), {
    name: 'session-storage'
}));
/**
 * Calculate stats for a single session
 */ function calculateSessionStats(session) {
    const { attentionTimeline, workMinutes } = session;
    // Average attention score
    const avgAttention = attentionTimeline.reduce((sum, score)=>sum + score, 0) / attentionTimeline.length;
    // Find most distracted minute
    let mostDistractedMinute = null;
    let lowestAvg = 1;
    // Group by minute and find lowest
    for(let min = 0; min < workMinutes; min++){
        const startIdx = min * 60;
        const endIdx = Math.min(startIdx + 60, attentionTimeline.length);
        const minuteScores = attentionTimeline.slice(startIdx, endIdx);
        if (minuteScores.length > 0) {
            const minuteAvg = minuteScores.reduce((sum, score)=>sum + score, 0) / minuteScores.length;
            if (minuteAvg < lowestAvg) {
                lowestAvg = minuteAvg;
                mostDistractedMinute = min;
            }
        }
    }
    return {
        totalFocusTime: workMinutes,
        cyclesCompleted: 1,
        attentionScore: Math.round(avgAttention * 100),
        mostDistractedMinute
    };
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/dev/study-spark/src/store/pomodoroStore.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "usePomodoroStore",
    ()=>usePomodoroStore
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$zustand$2f$esm$2f$react$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/node_modules/zustand/esm/react.mjs [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$store$2f$settingsStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/src/store/settingsStore.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$store$2f$sessionStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/src/store/sessionStore.ts [app-client] (ecmascript)");
;
;
;
const usePomodoroStore = (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$zustand$2f$esm$2f$react$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["create"])((set, get)=>({
        // Initial state
        phase: 'idle',
        status: 'idle',
        timeRemaining: 0,
        cyclesCompleted: 0,
        currentTaskId: null,
        intervalId: null,
        startTimer: (taskId)=>{
            const settings = __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$store$2f$settingsStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useSettingsStore"].getState();
            const { intervalId } = get();
            // Clear any existing interval
            if (intervalId) {
                clearInterval(intervalId);
            }
            // Start work phase
            const newIntervalId = window.setInterval(()=>{
                get().tick();
            }, 1000);
            set({
                phase: 'work',
                status: 'running',
                timeRemaining: settings.workMin * 60,
                currentTaskId: taskId || null,
                intervalId: newIntervalId
            });
        },
        pauseTimer: ()=>{
            const { intervalId } = get();
            if (intervalId) {
                clearInterval(intervalId);
            }
            set({
                status: 'paused',
                intervalId: null
            });
        },
        resumeTimer: ()=>{
            const { status } = get();
            if (status !== 'paused') return;
            const newIntervalId = window.setInterval(()=>{
                get().tick();
            }, 1000);
            set({
                status: 'running',
                intervalId: newIntervalId
            });
        },
        skipPhase: ()=>{
            // Force move to next phase
            set({
                timeRemaining: 0
            });
            get().tick();
        },
        resetTimer: ()=>{
            const { intervalId } = get();
            if (intervalId) {
                clearInterval(intervalId);
            }
            set({
                phase: 'idle',
                status: 'idle',
                timeRemaining: 0,
                cyclesCompleted: 0,
                currentTaskId: null,
                intervalId: null
            });
        },
        tick: ()=>{
            const state = get();
            const settings = __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$store$2f$settingsStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useSettingsStore"].getState();
            if (state.status !== 'running') return;
            // Countdown
            if (state.timeRemaining > 0) {
                set({
                    timeRemaining: state.timeRemaining - 1
                });
                return;
            }
            // Phase completed - determine next phase
            let nextPhase;
            let nextDuration;
            let newCyclesCompleted = state.cyclesCompleted;
            if (state.phase === 'work') {
                // Work completed
                const sessionStore = __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$store$2f$sessionStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useSessionStore"].getState();
                sessionStore.addSession({
                    taskId: state.currentTaskId,
                    date: new Date().toISOString().split('T')[0],
                    workMinutes: settings.workMin,
                    breakMinutes: 0,
                    attentionTimeline: sessionStore.currentAttentionTimeline
                });
                sessionStore.clearCurrentTimeline();
                newCyclesCompleted += 1;
                // Long break after cyclesToLong cycles, otherwise short break
                if (newCyclesCompleted % settings.cyclesToLong === 0) {
                    nextPhase = 'longBreak';
                    nextDuration = settings.longBreak * 60;
                } else {
                    nextPhase = 'shortBreak';
                    nextDuration = settings.shortBreak * 60;
                }
            } else {
                // Break completed - back to work
                nextPhase = 'work';
                nextDuration = settings.workMin * 60;
            }
            // TODO: Play sound notification here
            // TODO: Log session to sessionStore here
            set({
                phase: nextPhase,
                timeRemaining: nextDuration,
                cyclesCompleted: newCyclesCompleted
            });
        }
    }));
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/dev/study-spark/src/hooks/usePomodoroTest.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "usePomodoroTest",
    ()=>usePomodoroTest
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$store$2f$pomodoroStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/src/store/pomodoroStore.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$store$2f$sessionStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/src/store/sessionStore.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$store$2f$settingsStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/src/store/settingsStore.ts [app-client] (ecmascript)");
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
;
function usePomodoroTest() {
    _s();
    const pomodoro = (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$store$2f$pomodoroStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["usePomodoroStore"])();
    const session = (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$store$2f$sessionStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useSessionStore"])();
    const settings = (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$store$2f$settingsStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useSettingsStore"])();
    // Simulate attention tracking during work phases
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "usePomodoroTest.useEffect": ()=>{
            if (pomodoro.status !== 'running' || pomodoro.phase !== 'work') {
                return;
            }
            // Record fake attention score every second
            const interval = setInterval({
                "usePomodoroTest.useEffect.interval": ()=>{
                    // Generate random attention score between 0.7 and 1.0
                    const fakeAttentionScore = 0.7 + Math.random() * 0.3;
                    session.recordAttention(fakeAttentionScore);
                }
            }["usePomodoroTest.useEffect.interval"], 1000);
            return ({
                "usePomodoroTest.useEffect": ()=>clearInterval(interval)
            })["usePomodoroTest.useEffect"];
        }
    }["usePomodoroTest.useEffect"], [
        pomodoro.status,
        pomodoro.phase,
        session
    ]);
    return {
        // Pomodoro controls
        startTimer: pomodoro.startTimer,
        pauseTimer: pomodoro.pauseTimer,
        resumeTimer: pomodoro.resumeTimer,
        skipPhase: pomodoro.skipPhase,
        resetTimer: pomodoro.resetTimer,
        // Current state
        phase: pomodoro.phase,
        status: pomodoro.status,
        timeRemaining: pomodoro.timeRemaining,
        cyclesCompleted: pomodoro.cyclesCompleted,
        // Session data
        sessions: session.sessions,
        todayStats: session.getTodayStats(),
        // Settings
        settings: settings,
        updateSettings: settings.updateSettings,
        // Helpers for testing
        simulateFullCycle: ()=>{
            // Speed up timer for testing (5 second work, 2 second break)
            settings.updateSettings({
                workMin: 0.083,
                shortBreak: 0.033,
                longBreak: 0.05
            });
            pomodoro.startTimer('test-task-123');
        },
        resetToDefaults: ()=>{
            pomodoro.resetTimer();
            settings.resetSettings();
        }
    };
}
_s(usePomodoroTest, "U26mxfDDb9H7Xg7X0yA9AExQPTw=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$store$2f$pomodoroStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["usePomodoroStore"],
        __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$store$2f$sessionStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useSessionStore"],
        __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$store$2f$settingsStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useSettingsStore"]
    ];
});
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/dev/study-spark/src/lib/utils.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "cn",
    ()=>cn
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$clsx$2f$dist$2f$clsx$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/node_modules/clsx/dist/clsx.mjs [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$tailwind$2d$merge$2f$dist$2f$bundle$2d$mjs$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/node_modules/tailwind-merge/dist/bundle-mjs.mjs [app-client] (ecmascript)");
;
;
function cn() {
    for(var _len = arguments.length, inputs = new Array(_len), _key = 0; _key < _len; _key++){
        inputs[_key] = arguments[_key];
    }
    return (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$tailwind$2d$merge$2f$dist$2f$bundle$2d$mjs$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["twMerge"])((0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$clsx$2f$dist$2f$clsx$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["clsx"])(inputs));
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/dev/study-spark/src/components/ui/button.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Button",
    ()=>Button,
    "buttonVariants",
    ()=>buttonVariants
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f40$radix$2d$ui$2f$react$2d$slot$2f$dist$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/node_modules/@radix-ui/react-slot/dist/index.mjs [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$class$2d$variance$2d$authority$2f$dist$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/node_modules/class-variance-authority/dist/index.mjs [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/src/lib/utils.ts [app-client] (ecmascript)");
;
;
;
;
;
const buttonVariants = (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$class$2d$variance$2d$authority$2f$dist$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["cva"])("inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0", {
    variants: {
        variant: {
            default: "bg-primary text-primary-foreground shadow hover:bg-primary/90",
            destructive: "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
            outline: "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
            secondary: "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
            ghost: "hover:bg-accent hover:text-accent-foreground",
            link: "text-primary underline-offset-4 hover:underline"
        },
        size: {
            default: "h-9 px-4 py-2",
            sm: "h-8 rounded-md px-3 text-xs",
            lg: "h-10 rounded-md px-8",
            icon: "h-9 w-9"
        }
    },
    defaultVariants: {
        variant: "default",
        size: "default"
    }
});
const Button = /*#__PURE__*/ __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["forwardRef"](_c = (param, ref)=>{
    let { className, variant, size, asChild = false, ...props } = param;
    const Comp = asChild ? __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f40$radix$2d$ui$2f$react$2d$slot$2f$dist$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Slot"] : "button";
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(Comp, {
        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["cn"])(buttonVariants({
            variant,
            size,
            className
        })),
        ref: ref,
        ...props
    }, void 0, false, {
        fileName: "[project]/dev/study-spark/src/components/ui/button.tsx",
        lineNumber: 47,
        columnNumber: 7
    }, ("TURBOPACK compile-time value", void 0));
});
_c1 = Button;
Button.displayName = "Button";
;
var _c, _c1;
__turbopack_context__.k.register(_c, "Button$React.forwardRef");
__turbopack_context__.k.register(_c1, "Button");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/dev/study-spark/src/lib/pomodoro/timer.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * Convert seconds to MM:SS format
 */ __turbopack_context__.s([
    "formatTime",
    ()=>formatTime,
    "getPhaseDuration",
    ()=>getPhaseDuration,
    "getPhaseLabel",
    ()=>getPhaseLabel,
    "getProgress",
    ()=>getProgress
]);
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return "".concat(mins.toString().padStart(2, '0'), ":").concat(secs.toString().padStart(2, '0'));
}
function getProgress(timeRemaining, totalTime) {
    if (totalTime === 0) return 0;
    return (totalTime - timeRemaining) / totalTime * 100;
}
function getPhaseLabel(phase) {
    switch(phase){
        case 'work':
            return 'Focus Time';
        case 'shortBreak':
            return 'Short Break';
        case 'longBreak':
            return 'Long Break';
        default:
            return 'Ready';
    }
}
function getPhaseDuration(phase, settings) {
    switch(phase){
        case 'work':
            return settings.workMin * 60;
        case 'shortBreak':
            return settings.shortBreak * 60;
        case 'longBreak':
            return settings.longBreak * 60;
        default:
            return 0;
    }
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/dev/study-spark/src/app/test/page.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>TestPage
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$hooks$2f$usePomodoroTest$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/src/hooks/usePomodoroTest.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$components$2f$ui$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/src/components/ui/button.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$lib$2f$pomodoro$2f$timer$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/dev/study-spark/src/lib/pomodoro/timer.ts [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
function TestPage() {
    _s();
    const { // Controls
    startTimer, pauseTimer, resumeTimer, skipPhase, resetTimer, // State
    phase, status, timeRemaining, cyclesCompleted, // Data
    sessions, todayStats, settings } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$hooks$2f$usePomodoroTest$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["usePomodoroTest"])();
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("main", {
        className: "container max-w-4xl mx-auto py-8 px-4",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                className: "text-3xl font-bold mb-8",
                children: "Pomodoro Test Page"
            }, void 0, false, {
                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                lineNumber: 31,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "bg-gray-100 p-8 rounded-lg mb-6",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "text-center",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "text-sm text-gray-600 mb-2",
                            children: "Phase"
                        }, void 0, false, {
                            fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                            lineNumber: 36,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "text-2xl font-bold mb-4 capitalize",
                            children: phase
                        }, void 0, false, {
                            fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                            lineNumber: 37,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "text-sm text-gray-600 mb-2",
                            children: "Time Remaining"
                        }, void 0, false, {
                            fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                            lineNumber: 39,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "text-6xl font-bold mb-4 font-mono",
                            children: (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$lib$2f$pomodoro$2f$timer$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["formatTime"])(timeRemaining)
                        }, void 0, false, {
                            fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                            lineNumber: 40,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "text-sm text-gray-600 mb-2",
                            children: "Status"
                        }, void 0, false, {
                            fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                            lineNumber: 42,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "text-xl font-semibold capitalize mb-4",
                            children: status
                        }, void 0, false, {
                            fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                            lineNumber: 43,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "text-sm text-gray-600 mb-2",
                            children: "Cycles Completed"
                        }, void 0, false, {
                            fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                            lineNumber: 45,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "text-xl font-semibold",
                            children: cyclesCompleted
                        }, void 0, false, {
                            fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                            lineNumber: 46,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                    lineNumber: 35,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                lineNumber: 34,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "grid grid-cols-2 md:grid-cols-4 gap-3 mb-6",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$components$2f$ui$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                        onClick: ()=>startTimer('test-task'),
                        disabled: status === 'running',
                        children: "Start Timer"
                    }, void 0, false, {
                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                        lineNumber: 52,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$components$2f$ui$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                        onClick: pauseTimer,
                        disabled: status !== 'running',
                        children: "Pause"
                    }, void 0, false, {
                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                        lineNumber: 55,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$components$2f$ui$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                        onClick: resumeTimer,
                        disabled: status !== 'paused',
                        children: "Resume"
                    }, void 0, false, {
                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                        lineNumber: 58,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$components$2f$ui$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                        onClick: skipPhase,
                        disabled: status === 'idle',
                        children: "Skip Phase"
                    }, void 0, false, {
                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                        lineNumber: 61,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                lineNumber: 51,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-6",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$components$2f$ui$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                    onClick: resetTimer,
                    variant: "destructive",
                    className: "w-full",
                    children: "Reset Timer"
                }, void 0, false, {
                    fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                    lineNumber: 67,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                lineNumber: 66,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "bg-blue-50 p-6 rounded-lg mb-6",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                        className: "text-xl font-bold mb-4",
                        children: "Today's Stats"
                    }, void 0, false, {
                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                        lineNumber: 74,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "grid grid-cols-2 md:grid-cols-4 gap-4",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-sm text-gray-600",
                                        children: "Total Focus Time"
                                    }, void 0, false, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 77,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-2xl font-bold",
                                        children: [
                                            todayStats.totalFocusTime,
                                            "m"
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 78,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                lineNumber: 76,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-sm text-gray-600",
                                        children: "Cycles Completed"
                                    }, void 0, false, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 81,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-2xl font-bold",
                                        children: todayStats.cyclesCompleted
                                    }, void 0, false, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 82,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                lineNumber: 80,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-sm text-gray-600",
                                        children: "Attention Score"
                                    }, void 0, false, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 85,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-2xl font-bold",
                                        children: [
                                            todayStats.attentionScore,
                                            "%"
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 86,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                lineNumber: 84,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-sm text-gray-600",
                                        children: "Most Distracted"
                                    }, void 0, false, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 89,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-2xl font-bold",
                                        children: todayStats.mostDistractedMinute !== null ? "Min ".concat(todayStats.mostDistractedMinute) : 'N/A'
                                    }, void 0, false, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 90,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                lineNumber: 88,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                        lineNumber: 75,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                lineNumber: 73,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "bg-gray-50 p-6 rounded-lg mb-6",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                        className: "text-xl font-bold mb-4",
                        children: "Current Settings"
                    }, void 0, false, {
                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                        lineNumber: 101,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "grid grid-cols-2 md:grid-cols-3 gap-4 text-sm",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-gray-600",
                                        children: "Work Duration"
                                    }, void 0, false, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 104,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "font-semibold",
                                        children: [
                                            settings.workMin,
                                            " min"
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 105,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                lineNumber: 103,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-gray-600",
                                        children: "Short Break"
                                    }, void 0, false, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 108,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "font-semibold",
                                        children: [
                                            settings.shortBreak,
                                            " min"
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 109,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                lineNumber: 107,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-gray-600",
                                        children: "Long Break"
                                    }, void 0, false, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 112,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "font-semibold",
                                        children: [
                                            settings.longBreak,
                                            " min"
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 113,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                lineNumber: 111,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-gray-600",
                                        children: "Cycles to Long"
                                    }, void 0, false, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 116,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "font-semibold",
                                        children: settings.cyclesToLong
                                    }, void 0, false, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 117,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                lineNumber: 115,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-gray-600",
                                        children: "Adaptive"
                                    }, void 0, false, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 120,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "font-semibold",
                                        children: settings.adaptiveEnabled ? 'On' : 'Off'
                                    }, void 0, false, {
                                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                        lineNumber: 121,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                lineNumber: 119,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                        lineNumber: 102,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                lineNumber: 100,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "bg-white border rounded-lg p-6",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                        className: "text-xl font-bold mb-4",
                        children: [
                            "Session History (",
                            sessions.length,
                            ")"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                        lineNumber: 128,
                        columnNumber: 9
                    }, this),
                    sessions.length === 0 ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "text-gray-500",
                        children: "No sessions yet. Complete a work session to see data here."
                    }, void 0, false, {
                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                        lineNumber: 130,
                        columnNumber: 11
                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "space-y-3",
                        children: sessions.slice(-10).reverse().map((session)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "border-l-4 border-blue-500 pl-4 py-2",
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "flex justify-between items-start",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                    className: "font-semibold",
                                                    children: new Date(session.date).toLocaleString()
                                                }, void 0, false, {
                                                    fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                                    lineNumber: 137,
                                                    columnNumber: 21
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                    className: "text-sm text-gray-600",
                                                    children: [
                                                        "Work: ",
                                                        session.workMinutes,
                                                        "m | Task ID: ",
                                                        session.taskId || 'None'
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                                    lineNumber: 140,
                                                    columnNumber: 21
                                                }, this)
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                            lineNumber: 136,
                                            columnNumber: 19
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "text-right",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                    className: "text-sm text-gray-600",
                                                    children: "Attention Data"
                                                }, void 0, false, {
                                                    fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                                    lineNumber: 146,
                                                    columnNumber: 21
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                    className: "font-semibold",
                                                    children: [
                                                        session.attentionTimeline.length,
                                                        " samples"
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                                    lineNumber: 147,
                                                    columnNumber: 21
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                    className: "text-sm",
                                                    children: [
                                                        "Avg: ",
                                                        Math.round(session.attentionTimeline.reduce((a, b)=>a + b, 0) / session.attentionTimeline.length * 100),
                                                        "%"
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                                    lineNumber: 150,
                                                    columnNumber: 21
                                                }, this)
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                            lineNumber: 145,
                                            columnNumber: 19
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                    lineNumber: 135,
                                    columnNumber: 17
                                }, this)
                            }, session.id, false, {
                                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                lineNumber: 134,
                                columnNumber: 15
                            }, this))
                    }, void 0, false, {
                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                        lineNumber: 132,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                lineNumber: 127,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                        className: "font-bold mb-2",
                        children: "Testing Instructions:"
                    }, void 0, false, {
                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                        lineNumber: 166,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("ol", {
                        className: "list-decimal list-inside space-y-1 text-sm",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                                children: 'Click "Start Timer" to begin a work session'
                            }, void 0, false, {
                                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                lineNumber: 168,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                                children: 'Use "Skip Phase" to fast-forward through phases'
                            }, void 0, false, {
                                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                lineNumber: 169,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                                children: 'Check "Session History" after completing work sessions'
                            }, void 0, false, {
                                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                lineNumber: 170,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                                children: "Verify attention data is being recorded automatically"
                            }, void 0, false, {
                                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                lineNumber: 171,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                                children: "Test Pause/Resume functionality"
                            }, void 0, false, {
                                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                                lineNumber: 172,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                        lineNumber: 167,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
                lineNumber: 165,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/dev/study-spark/src/app/test/page.tsx",
        lineNumber: 30,
        columnNumber: 5
    }, this);
}
_s(TestPage, "3eRSqowL6nPt6ivHC3p9QMeRAWE=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$dev$2f$study$2d$spark$2f$src$2f$hooks$2f$usePomodoroTest$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["usePomodoroTest"]
    ];
});
_c = TestPage;
var _c;
__turbopack_context__.k.register(_c, "TestPage");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]);

//# sourceMappingURL=dev_study-spark_src_07714825._.js.map