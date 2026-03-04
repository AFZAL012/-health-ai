import { Container, Box, Typography, Paper, Button, Grid, Alert, Divider, Stack } from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import DoneAllIcon from '@mui/icons-material/DoneAll';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ShareIcon from '@mui/icons-material/Share';

const ResultsPage = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const prediction = location.state?.prediction;

    if (!prediction) {
        return (
            <Container maxWidth="sm" sx={{ py: 12, textAlign: 'center' }}>
                <Typography variant="h5" gutterBottom>No results found</Typography>
                <Button variant="contained" onClick={() => navigate('/analyze')} sx={{ mt: 3, bgcolor: '#452829' }}>
                    Back to Analysis
                </Button>
            </Container>
        );
    }

    return (
        <Container maxWidth="md" sx={{ py: 10 }}>
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
            >
                <Box sx={{ mb: 6, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Button
                        startIcon={<ArrowBackIcon />}
                        onClick={() => navigate('/analyze')}
                        sx={{ color: '#452829', fontWeight: 600 }}
                    >
                        New Analysis
                    </Button>
                    <Button
                        startIcon={<ShareIcon />}
                        variant="outlined"
                        sx={{ borderColor: 'rgba(69, 40, 41, 0.2)', color: '#452829', borderRadius: 3 }}
                    >
                        Safe Share
                    </Button>
                </Box>

                <Paper
                    elevation={0}
                    className="glass-panel"
                    sx={{ borderRadius: 6, overflow: 'hidden' }}
                >
                    {/* Header */}
                    <Box sx={{ p: 4, bgcolor: '#452829', color: 'white', display: 'flex', alignItems: 'center', gap: 2 }}>
                        <DoneAllIcon sx={{ fontSize: 32, color: '#E8D1C5' }} />
                        <Typography variant="h5" sx={{ fontWeight: 800, fontFamily: "'Outfit', sans-serif" }}>
                            Analysis Results Summary
                        </Typography>
                    </Box>

                    <Box sx={{ p: 6 }}>
                        {/* Primary Suggestion Section */}
                        <Box sx={{ mb: 6, textAlign: 'center' }}>
                            <Typography variant="overline" sx={{ letterSpacing: 3, fontWeight: 700, color: 'text.secondary' }}>
                                PRIMARY SUGGESTION
                            </Typography>
                            <Typography variant="h2" sx={{ my: 2, color: '#452829', fontWeight: 900, fontFamily: "'Outfit', sans-serif" }}>
                                {prediction.prediction}
                            </Typography>
                            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1, mt: 1 }}>
                                <DoneAllIcon sx={{ color: 'success.main', fontSize: 20 }} />
                                <Typography variant="body1" sx={{ fontWeight: 600, color: 'success.main' }}>
                                    Diagnosis Analysis Match
                                </Typography>
                            </Box>
                        </Box>

                        <Divider sx={{ my: 6, opacity: 0.1 }} />

                        <Grid container spacing={4}>
                            <Grid item xs={12} md={7}>
                                <Typography variant="h6" gutterBottom sx={{ fontWeight: 800, color: '#452829' }}>Clinical Context</Typography>
                                <Typography variant="body1" sx={{ color: 'text.secondary', lineHeight: 1.8, mb: 4 }}>
                                    Based on the symptoms provided, our AI has identified a strong correlation with **{prediction.prediction}**. This is a preliminary assessment and should be used to guide professional medical consultation.
                                </Typography>

                                <Box sx={{ p: 3, bgcolor: 'rgba(69, 40, 41, 0.03)', borderRadius: 4, borderLeft: '4px solid #452829' }}>
                                    <Typography variant="subtitle2" sx={{ fontWeight: 800, mb: 1 }}>Recommended Next Steps:</Typography>
                                    <ul style={{ paddingLeft: '20px', margin: 0, color: '#57595B' }}>
                                        <li>Monitor symptoms for the next 24-48 hours.</li>
                                        <li>Maintain hydration and rest.</li>
                                        <li>Document any changes in frequency or intensity.</li>
                                    </ul>
                                </Box>
                            </Grid>

                            <Grid item xs={12} md={5}>
                                <Paper elevation={0} sx={{ p: 3, borderRadius: 4, bgcolor: '#F3E8DF', height: '100%', border: '1px solid rgba(69, 40, 41, 0.05)' }}>
                                    <Typography variant="subtitle1" sx={{ fontWeight: 800, mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                                        <LocalHospitalIcon sx={{ color: '#452829' }} /> Medical Referral
                                    </Typography>
                                    <Typography variant="body2" sx={{ color: 'text.secondary', lineHeight: 1.6, mb: 3 }}>
                                        We recommend discussing these results with a board-certified professional.
                                    </Typography>
                                    <Stack spacing={2}>
                                        <Button variant="contained" fullWidth sx={{ bgcolor: '#452829', borderRadius: 2, py: 1 }}>
                                            Find a Doctor
                                        </Button>
                                        <Button variant="outlined" fullWidth sx={{ borderColor: 'rgba(69, 40, 41, 0.2)', color: '#452829', borderRadius: 2, py: 1 }}>
                                            Telehealth Visit
                                        </Button>
                                    </Stack>
                                </Paper>
                            </Grid>
                        </Grid>

                        <Alert
                            severity="warning"
                            icon={<WarningAmberIcon style={{ color: '#452829' }} />}
                            sx={{
                                mt: 6,
                                borderRadius: 4,
                                bgcolor: 'rgba(232, 209, 197, 0.3)',
                                color: '#452829',
                                border: '1px solid rgba(232, 209, 197, 0.5)',
                                '& .MuiAlert-icon': { p: 0.5 }
                            }}
                        >
                            <Typography variant="caption" sx={{ fontWeight: 600, display: 'block' }}>IMPORTANT DISCLAIMER</Typography>
                            This analysis is generated by an artificial intelligence and is **not** a formal medical diagnosis. If you are experiencing a medical emergency, please call your local emergency services immediately.
                        </Alert>
                    </Box>
                </Paper>

                <Box sx={{ mt: 6, textAlign: 'center' }}>
                    <Typography variant="caption" color="text.secondary">
                        Analysis ID: {prediction.analysisId || 'MD-8829-X'} • Generated on {new Date().toLocaleDateString()}
                    </Typography>
                </Box>
            </motion.div>
        </Container>
    );
};

export default ResultsPage;
