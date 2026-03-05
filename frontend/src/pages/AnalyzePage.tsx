import { useState } from 'react';
import { Container, Box, Typography, Button, Paper, Grid, Chip, CircularProgress, Stack, Divider, Avatar } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import BiotechIcon from '@mui/icons-material/Biotech';
import SecurityIcon from '@mui/icons-material/Security';
import ScienceIcon from '@mui/icons-material/Science';

const symptomCategories = [
    {
        name: 'General',
        symptoms: ['Fever', 'Fatigue', 'Headache', 'Chills', 'Dizziness']
    },
    {
        name: 'Respiratory',
        symptoms: ['Cough', 'Shortness of Breath', 'Sore Throat']
    },
    {
        name: 'Digestive',
        symptoms: ['Nausea', 'Stomach Pain', 'Vomiting']
    },
    {
        name: 'Pain & Physical',
        symptoms: ['Body Ache', 'Chest Pain', 'Joint Pain', 'Muscle Cramps']
    }
];

const AnalyzePage = () => {
    const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    const toggleSymptom = (symptom: string) => {
        setSelectedSymptoms(prev =>
            prev.includes(symptom)
                ? prev.filter(s => s !== symptom)
                : [...prev, symptom]
        );
    };

    const handleAnalyze = async () => {
        if (selectedSymptoms.length === 0) {
            setError('Please select at least one symptom.');
            return;
        }

        setIsLoading(true);
        setError(null);

        try {
            const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/v1/predict/analyze`, {
                symptoms: selectedSymptoms.join(', ')
            });

            const analysisId = response.data.analysisId || 'temp-' + Date.now();
            navigate(`/results/${analysisId}`, { state: { prediction: response.data } });
        } catch (err: any) {
            setError(err.response?.data?.error?.message || 'An error occurred during analysis.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Box sx={{ minHeight: '100vh', pt: { xs: 8, md: 12 }, pb: 8, bgcolor: '#F3E8DF' }}>
            <Container maxWidth="xl">
                <Grid container spacing={4}>
                    {/* Left Panel: Clinical Context */}
                    <Grid item xs={12} md={5}>
                        <motion.div
                            initial={{ opacity: 0, x: -30 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.8 }}
                        >
                            <Box sx={{ pr: { md: 4 } }}>
                                <Box sx={{
                                    display: 'inline-flex',
                                    p: 1.5,
                                    borderRadius: '16px',
                                    bgcolor: '#2D1B1C',
                                    color: 'white',
                                    mb: 4
                                }}>
                                    <ScienceIcon />
                                </Box>
                                <Typography variant="h2" sx={{ fontWeight: 900, mb: 2, fontFamily: "'Outfit', sans-serif" }}>
                                    Neural <span style={{ color: '#C5A898' }}>Diagnostics.</span>
                                </Typography>
                                <Typography variant="h6" sx={{ color: 'text.secondary', fontWeight: 400, mb: 6, lineHeight: 1.6 }}>
                                    Experience the future of healthcare screening. Our AI models analyze symptoms in real-time using patterns derived from millions of clinical data points.
                                </Typography>

                                <Stack spacing={3} sx={{ mb: 6 }}>
                                    {[
                                        { icon: <BiotechIcon />, title: 'Bio-Encoding', desc: 'Symptom weightage based on clinical frequency.' },
                                        { icon: <SecurityIcon />, title: 'Encrypted Vault', desc: 'Secure transit for sensitive health data.' },
                                        { icon: <HealthAndSafetyIcon />, title: 'Guidance Only', desc: 'AI results provided for preliminary guidance.' }
                                    ].map((item, i) => (
                                        <Box key={i} sx={{ display: 'flex', gap: 2 }}>
                                            <Avatar sx={{ bgcolor: 'white', border: '1px solid rgba(0,0,0,0.05)', color: '#452829' }}>
                                                {item.icon}
                                            </Avatar>
                                            <Box>
                                                <Typography variant="subtitle1" sx={{ fontWeight: 800 }}>{item.title}</Typography>
                                                <Typography variant="body2" sx={{ color: 'text.secondary' }}>{item.desc}</Typography>
                                            </Box>
                                        </Box>
                                    ))}
                                </Stack>

                                <Paper sx={{
                                    p: 0,
                                    borderRadius: '30px',
                                    overflow: 'hidden',
                                    height: '340px',
                                    display: { xs: 'none', md: 'block' },
                                    position: 'relative'
                                }}>
                                    <Box
                                        component="img"
                                        src="https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&q=80&w=1000"
                                        sx={{ width: '100%', height: '100%', objectFit: 'cover' }}
                                    />
                                    <Box sx={{
                                        position: 'absolute',
                                        bottom: 20,
                                        left: 20,
                                        right: 20,
                                        bgcolor: 'rgba(255,255,255,0.9)',
                                        backdropFilter: 'blur(10px)',
                                        p: 2,
                                        borderRadius: '16px',
                                        border: '1px solid rgba(0,0,0,0.05)'
                                    }}>
                                        <Typography variant="caption" sx={{ fontWeight: 800, color: '#452829' }}>NEURAL ENGINE v2.4-BETA</Typography>
                                        <Typography variant="body2" sx={{ color: 'text.secondary', fontSize: '0.75rem' }}>Active analysis mode enabled. Sub-millisecond latency.</Typography>
                                    </Box>
                                </Paper>
                            </Box>
                        </motion.div>
                    </Grid>

                    {/* Right Panel: Symptom Selector */}
                    <Grid item xs={12} md={7}>
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 0.6, delay: 0.2 }}
                        >
                            <Paper
                                elevation={0}
                                sx={{
                                    p: { xs: 4, md: 6 },
                                    borderRadius: '40px',
                                    bgcolor: 'white',
                                    boxShadow: '0 40px 80px rgba(69, 40, 41, 0.05)',
                                    border: '1px solid rgba(0,0,0,0.02)'
                                }}
                            >
                                <Typography variant="h5" sx={{ fontWeight: 900, mb: 1, fontFamily: "'Outfit', sans-serif" }}>
                                    Symptom Configuration
                                </Typography>
                                <Typography variant="body2" sx={{ color: 'text.secondary', mb: 5 }}>
                                    Select all elements that describe your current state.
                                </Typography>

                                {symptomCategories.map((category, idx) => (
                                    <Box key={category.name} sx={{ mb: 4 }}>
                                        <Typography variant="caption" sx={{ fontWeight: 900, letterSpacing: 1, color: 'text.disabled', mb: 2, display: 'block', textTransform: 'uppercase' }}>
                                            {category.name}
                                        </Typography>
                                        <Grid container spacing={1.5}>
                                            {category.symptoms.map((symptom) => {
                                                const isSelected = selectedSymptoms.includes(symptom);
                                                return (
                                                    <Grid item key={symptom}>
                                                        <Chip
                                                            label={symptom}
                                                            onClick={() => toggleSymptom(symptom)}
                                                            sx={{
                                                                px: 1.5,
                                                                py: 3,
                                                                borderRadius: '14px',
                                                                fontWeight: 700,
                                                                fontSize: '0.9rem',
                                                                bgcolor: isSelected ? '#2D1B1C' : '#F8F9FA',
                                                                color: isSelected ? 'white' : '#452829',
                                                                border: '1px solid',
                                                                borderColor: isSelected ? '#2D1B1C' : 'rgba(0,0,0,0.05)',
                                                                '&:hover': {
                                                                    bgcolor: isSelected ? '#1A1112' : '#EFF2F5',
                                                                },
                                                                transition: '0.2s cubic-bezier(0.4, 0, 0.2, 1)'
                                                            }}
                                                            icon={isSelected ? <CheckCircleOutlineIcon style={{ color: 'white', fontSize: '1.1rem' }} /> : undefined}
                                                        />
                                                    </Grid>
                                                );
                                            })}
                                        </Grid>
                                        {idx < symptomCategories.length - 1 && <Divider sx={{ mt: 4, opacity: 0.5 }} />}
                                    </Box>
                                ))}

                                <Box sx={{ mt: 6 }}>
                                    <AnimatePresence mode="wait">
                                        {error && (
                                            <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
                                                <Typography color="error" variant="body2" sx={{ fontWeight: 800, textAlign: 'center', mb: 3 }}>
                                                    {error}
                                                </Typography>
                                            </motion.div>
                                        )}
                                    </AnimatePresence>

                                    <Button
                                        fullWidth
                                        variant="contained"
                                        size="large"
                                        onClick={handleAnalyze}
                                        disabled={isLoading || selectedSymptoms.length === 0}
                                        sx={{
                                            py: 2.5,
                                            borderRadius: '16px',
                                            bgcolor: '#2D1B1C',
                                            color: 'white',
                                            fontSize: '1.1rem',
                                            fontWeight: 900,
                                            textTransform: 'none',
                                            boxShadow: '0 20px 40px rgba(0,0,0,0.2)',
                                            '&:hover': { bgcolor: '#000', transform: 'translateY(-2px)' },
                                            '&:disabled': { bgcolor: '#F0F0F0', color: '#B0B0B0' },
                                            transition: '0.3s cubic-bezier(0.4, 0, 0.2, 1)'
                                        }}
                                        startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <AnalyticsIcon />}
                                    >
                                        {isLoading ? 'Processing Neural Patterns...' : `Analyze ${selectedSymptoms.length} Symptom${selectedSymptoms.length !== 1 ? 's' : ''}`}
                                    </Button>

                                    <Typography variant="caption" sx={{ display: 'block', textAlign: 'center', mt: 3, color: 'text.disabled', fontWeight: 600 }}>
                                        By clicking analyze, you agree to our data processing guidelines.
                                    </Typography>
                                </Box>
                            </Paper>
                        </motion.div>
                    </Grid>
                </Grid>
            </Container>
        </Box>
    );
};

export default AnalyzePage;
