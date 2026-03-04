import { useState } from 'react';
import { Box, Typography, TextField, Button, Alert, Link as MuiLink, Grid, IconButton, InputAdornment, Stack, Avatar } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import { motion } from 'framer-motion';

const RegisterPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const { register } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        if (password !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        if (password.length < 8) {
            setError('Password must be at least 8 characters long');
            return;
        }

        setLoading(true);

        try {
            const profile = age || gender ? { age: age ? parseInt(age) : undefined, gender: gender || undefined } : undefined;
            const result = await register(email, password, profile);
            navigate('/verify-email', { state: { userId: result?.userId || result?.id } });
        } catch (err: any) {
            setError(err.message || 'Registration failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const benefits = [
        "Instant AI-driven diagnostic insights",
        "Secure patient history tracking",
        "Expert medical referral network",
        "Military-grade data encryption"
    ];

    return (
        <Box sx={{ minHeight: '100vh', display: 'flex' }}>
            <Grid container>
                {/* Left Side: Branding and Benefits */}
                <Grid item xs={12} md={6} sx={{
                    display: { xs: 'none', md: 'flex' },
                    position: 'relative',
                    bgcolor: '#452829',
                    color: 'white',
                    p: 8,
                    flexDirection: 'column',
                    justifyContent: 'center',
                    backgroundImage: 'url("https://images.unsplash.com/photo-1576091160550-217359f4ecf8?auto=format&fit=crop&q=80&w=2670")',
                    backgroundPosition: 'center',
                    backgroundSize: 'cover'
                }}>
                    <Box sx={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, bgcolor: 'rgba(69, 40, 41, 0.9)', zIndex: 1 }} />

                    <Box sx={{ position: 'relative', zIndex: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 8 }}>
                            <Box sx={{ p: 1, bgcolor: 'rgba(232, 209, 197, 0.2)', borderRadius: '12px', mr: 2 }}>
                                <LocalHospitalIcon sx={{ color: '#E8D1C5', fontSize: 32 }} />
                            </Box>
                            <Typography variant="h5" sx={{ fontWeight: 900, fontFamily: "'Outfit', sans-serif" }}>
                                MediDiagnose AI
                            </Typography>
                        </Box>

                        <Typography variant="h2" sx={{ fontWeight: 900, lineHeight: 1.1, mb: 6, fontFamily: "'Outfit', sans-serif" }}>
                            Join the Future of <br />
                            <span style={{ color: '#E8D1C5' }}>Personal Health.</span>
                        </Typography>

                        <Stack spacing={3}>
                            {benefits.map((benefit, i) => (
                                <Box key={i} sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                                    <CheckCircleOutlineIcon sx={{ color: '#E8D1C5' }} />
                                    <Typography variant="h6" sx={{ fontSize: '1.1rem', fontWeight: 500, color: 'rgba(255,255,255,0.8)' }}>
                                        {benefit}
                                    </Typography>
                                </Box>
                            ))}
                        </Stack>
                    </Box>
                </Grid>

                {/* Right Side: Registration Form */}
                <Grid item xs={12} md={6} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: '#F3E8DF', p: { xs: 3, md: 8 }, overflowY: 'auto' }}>
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.6 }}
                        style={{ width: '100%', maxWidth: '480px', padding: '40px 0' }}
                    >
                        <Box sx={{ mb: 6 }}>
                            <Typography variant="h4" sx={{ fontWeight: 900, fontFamily: "'Outfit', sans-serif", mb: 1.5, color: '#452829' }}>
                                Create Your Account
                            </Typography>
                            <Typography variant="body1" sx={{ color: '#57595B', fontWeight: 500 }}>
                                Start your health journey with a 2-minute setup.
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
                                    label="Email Address"
                                    type="email"
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    variant="outlined"
                                    sx={{ '& .MuiOutlinedInput-root': { borderRadius: 3, bgcolor: 'white' } }}
                                />

                                <Grid container spacing={2}>
                                    <Grid item xs={12} sm={6}>
                                        <TextField
                                            fullWidth
                                            label="Password"
                                            type={showPassword ? 'text' : 'password'}
                                            required
                                            value={password}
                                            onChange={(e) => setPassword(e.target.value)}
                                            InputProps={{
                                                endAdornment: (
                                                    <InputAdornment position="end">
                                                        <IconButton onClick={() => setShowPassword(!showPassword)} edge="end">
                                                            {showPassword ? <VisibilityOff /> : <Visibility />}
                                                        </IconButton>
                                                    </InputAdornment>
                                                ),
                                            }}
                                            sx={{ '& .MuiOutlinedInput-root': { borderRadius: 3, bgcolor: 'white' } }}
                                        />
                                    </Grid>
                                    <Grid item xs={12} sm={6}>
                                        <TextField
                                            fullWidth
                                            label="Confirm Password"
                                            type={showConfirmPassword ? 'text' : 'password'}
                                            required
                                            value={confirmPassword}
                                            onChange={(e) => setConfirmPassword(e.target.value)}
                                            InputProps={{
                                                endAdornment: (
                                                    <InputAdornment position="end">
                                                        <IconButton onClick={() => setShowConfirmPassword(!showConfirmPassword)} edge="end">
                                                            {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                                                        </IconButton>
                                                    </InputAdornment>
                                                ),
                                            }}
                                            sx={{ '& .MuiOutlinedInput-root': { borderRadius: 3, bgcolor: 'white' } }}
                                        />
                                    </Grid>
                                </Grid>

                                <Typography variant="subtitle2" sx={{ mt: 2, color: '#452829', fontWeight: 800 }}>
                                    PERSONAL DETAILS (OPTIONAL)
                                </Typography>

                                <Grid container spacing={2}>
                                    <Grid item xs={6}>
                                        <TextField
                                            fullWidth
                                            label="Age"
                                            type="number"
                                            value={age}
                                            onChange={(e) => setAge(e.target.value)}
                                            sx={{ '& .MuiOutlinedInput-root': { borderRadius: 3, bgcolor: 'white' } }}
                                        />
                                    </Grid>
                                    <Grid item xs={6}>
                                        <TextField
                                            fullWidth
                                            label="Gender"
                                            value={gender}
                                            onChange={(e) => setGender(e.target.value)}
                                            sx={{ '& .MuiOutlinedInput-root': { borderRadius: 3, bgcolor: 'white' } }}
                                        />
                                    </Grid>
                                </Grid>

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
                                    {loading ? <CircularProgress size={24} color="inherit" /> : 'Create Secure Account'}
                                </Button>
                            </Stack>

                            <Box sx={{ mt: 4, textAlign: 'center' }}>
                                <Typography variant="body2" sx={{ color: '#57595B', fontWeight: 500 }}>
                                    Already have an account?{' '}
                                    <MuiLink component={Link} to="/login" sx={{ color: '#452829', fontWeight: 700, textDecoration: 'none' }}>
                                        Log In
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

export default RegisterPage;
