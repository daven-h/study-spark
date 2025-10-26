(globalThis.TURBOPACK || (globalThis.TURBOPACK = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/Desktop/knighthacks25/study-spark/src/components/StarBorderButton.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>StarBorderButton
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/knighthacks25/study-spark/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/knighthacks25/study-spark/node_modules/next/dist/client/app-dir/link.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$clsx$2f$dist$2f$clsx$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/knighthacks25/study-spark/node_modules/clsx/dist/clsx.mjs [app-client] (ecmascript)");
"use client";
;
;
;
function StarBorderButton(param) {
    let { href, onClick, children, className, size = "lg", variant = "primary", ariaLabel } = param;
    const padding = size === "md" ? "py-[10px] px-[18px]" : "py-[12px] px-[22px]";
    const variantClasses = variant === "secondary" ? "star-inner-secondary" : "star-inner";
    const content = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "star-border-layer star-border-top",
                "aria-hidden": "true"
            }, void 0, false, {
                fileName: "[project]/Desktop/knighthacks25/study-spark/src/components/StarBorderButton.tsx",
                lineNumber: 36,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "star-border-layer star-border-bottom",
                "aria-hidden": "true"
            }, void 0, false, {
                fileName: "[project]/Desktop/knighthacks25/study-spark/src/components/StarBorderButton.tsx",
                lineNumber: 37,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$clsx$2f$dist$2f$clsx$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"])(variantClasses, "font-modular uppercase tracking-wide", padding),
                children: children
            }, void 0, false, {
                fileName: "[project]/Desktop/knighthacks25/study-spark/src/components/StarBorderButton.tsx",
                lineNumber: 39,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$clsx$2f$dist$2f$clsx$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"])("star-border-container", className),
        children: href ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
            href: href,
            "aria-label": ariaLabel !== null && ariaLabel !== void 0 ? ariaLabel : String(children),
            children: content
        }, void 0, false, {
            fileName: "[project]/Desktop/knighthacks25/study-spark/src/components/StarBorderButton.tsx",
            lineNumber: 54,
            columnNumber: 9
        }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$knighthacks25$2f$study$2d$spark$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
            type: "button",
            onClick: onClick,
            "aria-label": ariaLabel !== null && ariaLabel !== void 0 ? ariaLabel : String(children),
            children: content
        }, void 0, false, {
            fileName: "[project]/Desktop/knighthacks25/study-spark/src/components/StarBorderButton.tsx",
            lineNumber: 58,
            columnNumber: 9
        }, this)
    }, void 0, false, {
        fileName: "[project]/Desktop/knighthacks25/study-spark/src/components/StarBorderButton.tsx",
        lineNumber: 52,
        columnNumber: 5
    }, this);
}
_c = StarBorderButton;
var _c;
__turbopack_context__.k.register(_c, "StarBorderButton");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]);

//# sourceMappingURL=Desktop_knighthacks25_study-spark_src_components_StarBorderButton_tsx_faf3931f._.js.map