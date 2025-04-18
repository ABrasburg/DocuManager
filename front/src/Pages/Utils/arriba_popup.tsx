import { X } from "lucide-react";
import React from "react";

interface TopBarProps {
  title: string;
  onClose: () => void;
  icon?: React.ReactNode;
}

const TopBar: React.FC<TopBarProps> = ({ title, onClose, icon }) => {
  return (
    <div className="flex items-center justify-between bg-gray-100 p-3 border-b border-gray-300 rounded-t-lg">
      <div className="flex items-center gap-2">
        {icon && <span className="text-gray-600">{icon}</span>}
        <h2 className="text-gray-800 font-semibold text-lg">{title}</h2>
      </div>
      <button
        onClick={onClose}
        className="text-gray-600 hover:text-red-500 transition-colors"
        aria-label="Cerrar"
      >
        <X size={20} />
      </button>
    </div>
  );
};

export default TopBar;
