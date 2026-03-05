import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';

interface User {
    id: number;
    email: string;
    role: string;
    is_verified: boolean;
}

interface AuthContextType {
    user: User | null;
    accessToken: string | null;
    login: (email: string, password: string) => Promise<{ require_2fa?: boolean; challengeId?: number } | void>;
    verify2FA: (challengeId: number, otp: string) => Promise<void>;
    register: (email: string, password: string, profile?: any) => Promise<any>;
    logout: () => void;
    isAuthenticated: boolean;
    isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

interface AuthProviderProps {
    children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
    const [user, setUser] = useState<User | null>(null);
    const [accessToken, setAccessToken] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Load user from localStorage on mount
        const storedToken = localStorage.getItem('accessToken');
        const storedUser = localStorage.getItem('user');

        if (storedToken && storedUser) {
            setAccessToken(storedToken);
            setUser(JSON.parse(storedUser));

            // Set default axios header
            axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
        }

        // Add interceptor to handle 422/401 with "Subject must be a string"
        const interceptor = axios.interceptors.response.use(
            (response) => response,
            (error) => {
                const message = error.response?.data?.msg || error.response?.data?.error?.message;
                if (message === 'Subject must be a string') {
                    console.warn('Stale token detected, logging out...');
                    logout();
                }
                return Promise.reject(error);
            }
        );

        setIsLoading(false);

        return () => {
            axios.interceptors.response.eject(interceptor);
        };
    }, []);

    const login = async (email: string, password: string) => {
        try {
            const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/v1/auth/login`, {
                email,
                password,
            });

            if (response.data.require_2fa) {
                return { require_2fa: true, challengeId: response.data.challengeId };
            }

            const { accessToken: token, user: userData } = response.data;
            handleLoginSuccess(token, userData);
        } catch (error: any) {
            const errorData = error.response?.data?.error;
            let message = errorData?.message || 'Login failed';
            if (errorData?.details) {
                const details = Object.entries(errorData.details)
                    .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
                    .join('; ');
                message += ` (${details})`;
            }
            throw new Error(message);
        }
    };

    const verify2FA = async (challengeId: number, otp: string) => {
        try {
            const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/v1/auth/verify-2fa`, {
                challengeId,
                otp,
            });

            const { accessToken: token, user: userData } = response.data;
            handleLoginSuccess(token, userData);
        } catch (error: any) {
            const errorData = error.response?.data?.error;
            let message = errorData?.message || 'Verification failed';
            if (errorData?.details) {
                const details = Object.entries(errorData.details)
                    .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
                    .join('; ');
                message += ` (${details})`;
            }
            throw new Error(message);
        }
    };

    const handleLoginSuccess = (token: string, userData: User) => {
        setAccessToken(token);
        setUser(userData);

        // Store in localStorage
        localStorage.setItem('accessToken', token);
        localStorage.setItem('user', JSON.stringify(userData));

        // Set default axios header
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    };

    const register = async (email: string, password: string, profile?: any) => {
        try {
            const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/v1/auth/register`, {
                email,
                password,
                profile,
            });

            return response.data;
        } catch (error: any) {
            const errorData = error.response?.data?.error;
            let message = errorData?.message || 'Registration failed';
            if (errorData?.details) {
                const details = Object.entries(errorData.details)
                    .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
                    .join('; ');
                message += ` (${details})`;
            }
            throw new Error(message);
        }
    };

    const logout = () => {
        setUser(null);
        setAccessToken(null);
        localStorage.removeItem('accessToken');
        localStorage.removeItem('user');
        delete axios.defaults.headers.common['Authorization'];
    };

    const value = {
        user,
        accessToken,
        login,
        verify2FA,
        register,
        logout,
        isAuthenticated: !!user,
        isLoading,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
