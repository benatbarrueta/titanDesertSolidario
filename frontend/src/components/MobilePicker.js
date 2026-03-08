import React, { useEffect } from "react";
import "../styles/MobilePicker.css";

/**
 * MobilePicker
 * - Se usa como "input" clickable que abre un drawer con opciones grandes.
 * - No toca desktop: lo usaremos solo cuando isMobile sea true.
 */
export default function MobilePicker({
  label,
  placeholder = "Selecciona...",
  value,
  displayValue,
  options,
  isOpen,
  onOpen,
  onClose,
  onSelect,
  activeId,
}) {
  // Bloquear scroll del body mientras el drawer está abierto
  useEffect(() => {
    if (!isOpen) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = prev || "auto";
    };
  }, [isOpen]);

  return (
    <div className="mp-field">
      {label ? <div className="mp-label">{label}</div> : null}

      <button type="button" className="mp-trigger" onClick={onOpen}>
        <span className={`mp-trigger-text ${displayValue ? "" : "is-placeholder"}`}>
          {displayValue || placeholder}
        </span>
        <span className="mp-trigger-chevron">▾</span>
      </button>

      {isOpen && (
        <>
          <div className="mp-overlay" onClick={onClose} />

          <div className="mp-drawer" role="dialog" aria-modal="true">
            <div className="mp-drawer-header">
              <div className="mp-drawer-title">{label || "Selecciona"}</div>

              <button type="button" className="mp-close" onClick={onClose} aria-label="Cerrar">
                <span>×</span>
              </button>
            </div>

            <div className="mp-list">
              {options.map((opt) => {
                const isActive = String(opt.value) === String(activeId ?? value ?? "");
                return (
                  <button
                    key={opt.value}
                    type="button"
                    className={`mp-item ${isActive ? "active" : ""}`}
                    onClick={() => {
                      onSelect(opt.value);
                      onClose();
                    }}
                  >
                    <span className="mp-item-title">{opt.label}</span>
                    {opt.subLabel ? <span className="mp-item-sub">{opt.subLabel}</span> : null}
                  </button>
                );
              })}
            </div>
          </div>
        </>
      )}
    </div>
  );
}