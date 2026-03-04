import { useState } from 'react';
import { Box, Typography, TextField, Button, Alert, Paper, Link as MuiLink, CircularProgress, Grid, IconButton, InputAdornment, Stack, Avatar } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import { motion } from 'framer-motion';

const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const result = await login(email, password);
            if (result?.require_2fa) {
                navigate('/verify-2fa', { state: { challengeId: result.challengeId } });
            } else {
                navigate('/analyze');
            }
        } catch (err: any) {
            const errorMessage = err.message || 'Login failed. Please check your credentials.';
            setError(errorMessage);

            if (errorMessage.includes('not verified')) {
                navigate('/verify-email', { state: { challengeId: 'UNKNOWN' } });
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box sx={{ minHeight: '100vh', display: 'flex' }}>
            <Grid container>
                {/* Left Side: Image & Branding */}
                <Grid item xs={12} md={6} sx={{
                    display: { xs: 'none', md: 'flex' },
                    position: 'relative',
                    bgcolor: '#452829',
                    color: 'white',
                    p: 8,
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    backgroundImage: 'url("https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&q=80&w=2680")',
                    backgroundPosition: 'center',
                    backgroundSize: 'cover'
                }}>
                    <Box sx={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, bgcolor: 'rgba(69, 40, 41, 0.85)', zIndex: 1 }} />

                    <Box sx={{ position: 'relative', zIndex: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
                            <Box sx={{ p: 1, bgcolor: 'rgba(232, 209, 197, 0.2)', borderRadius: '12px', mr: 2 }}>
                                <LocalHospitalIcon sx={{ color: '#E8D1C5', fontSize: 32 }} />
                            </Box>
                            <Typography variant="h5" sx={{ fontWeight: 900, fontFamily: "'Outfit', sans-serif" }}>
                                MediDiagnose AI
                            </Typography>
                        </Box>

                        <Typography variant="h2" sx={{ fontWeight: 900, lineHeight: 1.1, mt: 10, fontFamily: "'Outfit', sans-serif" }}>
                            Securely Access Your <br />
                            <span style={{ color: '#E8D1C5' }}>Health Dashboard.</span>
                        </Typography>
                    </Box>

                    <Box sx={{ position: 'relative', zIndex: 2 }}>
                        <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.7)', mb: 2, maxWidth: 400 }}>
                            "The AI analysis provided me with a clear path forward before my doctor's appointment. Truly a game changer."
                        </Typography>
                        <Stack direction="row" spacing={2} alignItems="center">
                            <Avatar sx={{ width: 48, height: 48, border: '2px solid #E8D1C5' }} />
                            <Box>
                                <Typography variant="subtitle2" sx={{ fontWeight: 800 }}>Sarah Jenkins</Typography>
                                <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)' }}>Verified Patient</Typography>
                            </Box>
                        </Stack>
                    </Box>
                </Grid>

                {/* Right Side: Form */}
                <Grid item xs={12} md={6} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: '#F3E8DF', p: { xs: 3, md: 8 } }}>
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.6 }}
                        style={{ width: '100%', maxWidth: '440px' }}
                    >
                        <Box sx={{ mb: 6 }}>
                            <Typography variant="h4" sx={{ fontWeight: 900, fontFamily: "'Outfit', sans-serif", mb: 1.5, color: '#452829' }}>
                                Welcome Back
                            </Typography>
                            <Typography variant="body1" sx={{ color: '#57595B', fontWeight: 500 }}>
                                Enter your credentials to continue your analysis.
                            </Typography>
                        </Box>

                        {error && (
                            <Alert severity="error" sx={{ mb: 4, borderRadius: 3, bgcolor: 'rgba(211, 47, 47, 0.05)', color: '#d32f2f', border: '1px solid rgba(211, 47, 47, 0.1)' }}>
                                {error}
                            </Alert>
                        )}

                        <Box component="form" onSubmit={handleSubmit}>
                            <Stack spacing={3}>
                                <TextField
                                    fullWidth
                                    label="Email Account"
                                    type="email"
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    variant="outlined"
                                    autoComplete="email"
                                    sx={{
                                        '& .MuiOutlinedInput-root': { borderRadius: 3, bgcolor: 'white' },
                                        '& .MuiInputLabel-root': { color: '#57595B' }
                                    }}
                                />
                                <TextField
                                    fullWidth
                                    label="Password"
                                    type={showPassword ? 'text' : 'password'}
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    variant="outlined"
                                    autoComplete="current-password"
                                    sx={{
                                        '& .MuiOutlinedInput-root': { borderRadius: 3, bgcolor: 'white' },
                                        '& .MuiInputLabel-root': { color: '#57595B' }
                                    }}
                                    InputProps={{
                                        endAdornment: (
                                            <InputAdornment position="end">
                                                <IconButton onClick={() => setShowPassword(!showPassword)} edge="end">
                                                    {showPassword ? <VisibilityOff /> : <Visibility />}
                                                </IconButton>
                                            </InputAdornment>
                                        ),
                                    }}
                                />

                                <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                                    <MuiLink component={Link} to="#" sx={{ color: '#452829', fontWeight: 600, fontSize: '0.875rem', textDecoration: 'none' }}>
                                        Forgot Password?
                                    </MuiLink>
                                </Box>

                                <Button
                                    fullWidth
                                    type="submit"
                                    variant="contained"
                                    disabled={loading}
                                    className="button-premium"
                                    sx={{
                                        py: 2,
                                        fontSize: '1rem',
                                        fontWeight: 800,
                                        borderRadius: 4,
                                        bgcolor: '#452829',
                                        mt: 2,
                                        boxShadow: '0 12px 24px rgba(69, 40, 41, 0.2)',
                                        '&:hover': { bgcolor: '#57595B' }
                                    }}
                                >
                                    {loading ? <CircularProgress size={24} color="inherit" /> : 'Log In to Profile'}
                                </Button>
                            </Stack>

                            <Box sx={{ mt: 6, textAlign: 'center' }}>
                                <Typography variant="body2" sx={{ color: '#57595B', fontWeight: 500 }}>
                                    New to MediDiagnose?{' '}
                                    <MuiLink component={Link} to="/register" sx={{ color: '#452829', fontWeight: 700, textDecoration: 'none' }}>
                                        Create an Account
                                    </MuiLink>
                                </Typography>
                            </Box>
                        </Box>
                    </motion.div>
                </Grid>
            </Grid>
        </Box>
    );
};

export default LoginPage;
