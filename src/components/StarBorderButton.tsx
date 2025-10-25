"use client";

import Link from "next/link";
import clsx from "clsx";
import React from "react";

type Props = {
  href?: string;
  onClick?: () => void;
  children: React.ReactNode;
  className?: string;
  size?: "md" | "lg";
  variant?: "primary" | "secondary";
  ariaLabel?: string;
};

export default function StarBorderButton({
  href,
  onClick,
  children,
  className,
  size = "lg",
  variant = "primary",
  ariaLabel
}: Props) {
  const padding =
    size === "md" ? "py-[10px] px-[18px]" : "py-[12px] px-[22px]";

  const variantClasses = variant === "secondary" 
    ? "star-inner-secondary" 
    : "star-inner";

  const content = (
    <>
      {/* moving star layers */}
      <div className="star-border-layer star-border-top" aria-hidden="true" />
      <div className="star-border-layer star-border-bottom" aria-hidden="true" />
      {/* real button */}
      <span
        className={clsx(
          variantClasses,
          "font-modular uppercase tracking-wide",
          padding
        )}
      >
        {children}
      </span>
    </>
  );

  return (
    <span className={clsx("star-border-container", className)}>
      {href ? (
        <Link href={href} aria-label={ariaLabel ?? String(children)}>
          {content}
        </Link>
      ) : (
        <button type="button" onClick={onClick} aria-label={ariaLabel ?? String(children)}>
          {content}
        </button>
      )}
    </span>
  );
}
