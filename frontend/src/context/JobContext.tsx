'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { ProcessResponse } from '@/lib/api';

interface JobContextType {
    results: ProcessResponse | null;
    setResults: (results: ProcessResponse | null) => void;
    isLoading: boolean;
    setIsLoading: (loading: boolean) => void;
    error: string | null;
    setError: (error: string | null) => void;
}

const JobContext = createContext<JobContextType | undefined>(undefined);

export function JobProvider({ children }: { children: ReactNode }) {
    const [results, setResults] = useState<ProcessResponse | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    return (
        <JobContext.Provider value={{ results, setResults, isLoading, setIsLoading, error, setError }}>
            {children}
        </JobContext.Provider>
    );
}

export function useJob() {
    const context = useContext(JobContext);
    if (context === undefined) {
        throw new Error('useJob must be used within a JobProvider');
    }
    return context;
}
