import { createTheme } from '@mui/material/styles';

// Custom color palette
const colors = {
    primary: '#452829',      // Deep Burgundy
    secondary: '#57595B',    // Cool Gray
    sky: '#E8D1C5',          // Light Rose
    accent: '#E8D1C5',       // Light Rose
    background: '#F3E8DF',   // Cream
    white: '#FFFFFF',
    text: {
        primary: '#452829',
        secondary: '#57595B',
        light: '#6B7280',
    },
    success: '#10B981',
    warning: '#F59E0B',
    error: '#EF4444',
    info: '#E8D1C5',
};

export const theme = createTheme({
    palette: {
        primary: {
            main: colors.primary,
            light: colors.secondary,
            dark: '#140552',
            contrastText: colors.white,
        },
        secondary: {
            main: colors.secondary,
            light: colors.sky,
            dark: colors.primary,
            contrastText: colors.white,
        },
        background: {
            default: colors.background,
            paper: colors.white,
        },
        text: {
            primary: colors.text.primary,
            secondary: colors.text.secondary,
        },
        success: {
            main: colors.success,
        },
        warning: {
            main: colors.warning,
        },
        error: {
            main: colors.error,
        },
        info: {
            main: colors.info,
        },
    },
    typography: {
        fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
        h1: {
            fontSize: '2.5rem',
            fontWeight: 700,
            color: colors.primary,
            lineHeight: 1.2,
        },
        h2: {
            fontSize: '2rem',
            fontWeight: 600,
            color: colors.primary,
            lineHeight: 1.3,
        },
        h3: {
            fontSize: '1.75rem',
            fontWeight: 600,
            color: colors.primary,
            lineHeight: 1.4,
        },
        h4: {
            fontSize: '1.5rem',
            fontWeight: 600,
            color: colors.primary,
        },
        h5: {
            fontSize: '1.25rem',
            fontWeight: 600,
            color: colors.primary,
        },
        h6: {
            fontSize: '1rem',
            fontWeight: 600,
            color: colors.primary,
        },
        body1: {
            fontSize: '1rem',
            color: colors.text.primary,
        },
        body2: {
            fontSize: '0.875rem',
            color: colors.text.secondary,
        },
    },
    shape: {
        borderRadius: 12,
    },
    components: {
        MuiButton: {
            styleOverrides: {
                root: {
                    textTransform: 'none',
                    fontWeight: 600,
                    borderRadius: 8,
                    padding: '10px 24px',
                    boxShadow: 'none',
                    '&:hover': {
                        boxShadow: '0 4px 12px rgba(28, 7, 112, 0.2)',
                    },
                },
                contained: {
                    '&:hover': {
                        boxShadow: '0 6px 16px rgba(28, 7, 112, 0.25)',
                    },
                },
                containedPrimary: {
                    background: colors.primary,
                    '&:hover': {
                        background: '#140552',
                    },
                },
            },
        },
        MuiCard: {
            styleOverrides: {
                root: {
                    borderRadius: 16,
                    boxShadow: '0 4px 20px rgba(26, 50, 99, 0.08)',
                    '&:hover': {
                        boxShadow: '0 8px 30px rgba(26, 50, 99, 0.12)',
                    },
                },
            },
        },
        MuiTextField: {
            styleOverrides: {
                root: {
                    '& .MuiOutlinedInput-root': {
                        borderRadius: 8,
                        '&:hover fieldset': {
                            borderColor: colors.secondary,
                        },
                        '&.Mui-focused fieldset': {
                            borderColor: colors.primary,
                        },
                    },
                },
            },
        },
        MuiChip: {
            styleOverrides: {
                root: {
                    borderRadius: 8,
                    fontWeight: 500,
                },
                colorPrimary: {
                    backgroundColor: colors.primary,
                    color: colors.white,
                },
                colorSecondary: {
                    backgroundColor: colors.accent,
                    color: colors.primary,
                },
            },
        },
        MuiAlert: {
            styleOverrides: {
                root: {
                    borderRadius: 12,
                },
                standardSuccess: {
                    backgroundColor: '#ECFDF5',
                    color: colors.success,
                },
                standardError: {
                    backgroundColor: '#FEF2F2',
                    color: colors.error,
                },
                standardWarning: {
                    backgroundColor: '#FFFBEB',
                    color: colors.warning,
                },
                standardInfo: {
                    backgroundColor: '#EFF6FF',
                    color: colors.info,
                },
            },
        },
    },
});

export { colors };
