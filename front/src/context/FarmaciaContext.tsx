import React, { createContext, useContext, useState, useEffect } from 'react';

interface Farmacia {
  id: number;
  nombre: string;
}

interface FarmaciaContextType {
  farmacia: Farmacia | null;
  setFarmacia: (f: Farmacia | null) => void;
}

const FarmaciaContext = createContext<FarmaciaContextType>({
  farmacia: null,
  setFarmacia: () => {},
});

export const FarmaciaProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [farmacia, setFarmaciaState] = useState<Farmacia | null>(() => {
    try {
      const stored = localStorage.getItem('farmacia');
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  });

  const setFarmacia = (f: Farmacia | null) => {
    setFarmaciaState(f);
    if (f) {
      localStorage.setItem('farmacia', JSON.stringify(f));
    } else {
      localStorage.removeItem('farmacia');
    }
  };

  return (
    <FarmaciaContext.Provider value={{ farmacia, setFarmacia }}>
      {children}
    </FarmaciaContext.Provider>
  );
};

export const useFarmacia = () => useContext(FarmaciaContext);
