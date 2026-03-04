import { useState } from 'react';
import { Container, Box, Typography, TextField, Button, Paper, Alert, CircularProgress } from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import SecurityIcon from '@mui/icons-material/Security';

const TwoFactorPage = () => {
    const [otp, setOtp] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const location = useLocation();
    const navigate = useNavigate();
    const { verify2FA } = useAuth();

    // challengeId passed from Login page
    const challengeId = location.state?.challengeId;

    if (!challengeId) {
        navigate('/login');
        return null;
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (otp.length !== 6) {
            setError('Please enter a 6-digit code.');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            await verify2FA(challengeId, otp);
            navigate('/analyze');
        } catch (err: any) {
            setError(err.message || 'Invalid or expired verification code.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container maxWidth="sm" sx={{ py: 12 }}>
            <Paper elevation={3} sx={{ p: 6, borderRadius: 4 }}>
                <Box sx={{ textAlign: 'center' }}>
                    <SecurityIcon sx={{ fontSize: 64, color: '#452829', mb: 3 }} />
                    <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, color: '#452829' }}>
                        Two-Factor Authentication
                    </Typography>
                </Box>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 4, textAlign: 'center' }}>
                    We've sent a 6-digit verification code to your email. Please enter it below to continue.
                </Typography>

                {error && (
                    <Alert severity="error" sx={{ mb: 4, textAlign: 'left' }}>
                        {error}
                    </Alert>
                )}

                <Box component="form" onSubmit={handleSubmit}>
                    <TextField
                        fullWidth
                        label="Verification Code"
                        variant="outlined"
                        placeholder="123456"
                        value={otp}
                        onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
                        disabled={loading}
                        sx={{ mb: 4, '& input': { textAlign: 'center', fontSize: '1.5rem', letterSpacing: '0.5rem' } }}
                    />

                    <Button
                        fullWidth
                        type="submit"
                        variant="contained"
                        size="large"
                        disabled={loading}
                        sx={{
                            mt: 3,
                            py: 1.5,
                            fontSize: '1.1rem',
                            bgcolor: '#452829',
                            '&:hover': {
                                bgcolor: '#57595B',
                            },
                        }}
                    >
                        {loading ? <CircularProgress size={24} color="inherit" /> : 'Verify Code'}
                    </Button>
                </Box>

                <Button
                    sx={{ mt: 3, color: '#57595B' }}
                    onClick={() => navigate('/login')}
                >
                    Back to Login
                </Button>
            </Paper>
        </Container>
    );
};

export default TwoFactorPage;
