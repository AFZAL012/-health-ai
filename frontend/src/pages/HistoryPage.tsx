import { useState, useEffect } from 'react';
import { Container, Box, Typography, Paper, Grid, Card, CardContent, Button, Chip, CircularProgress, Alert, Stack, Avatar, IconButton } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import AssessmentIcon from '@mui/icons-material/Assessment';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import BarChartIcon from '@mui/icons-material/BarChart';
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import BiotechIcon from '@mui/icons-material/Biotech';

const HistoryPage = () => {
    const [history, setHistory] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const { accessToken, isAuthenticated } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        let isMounted = true;

        if (!isAuthenticated) {
            navigate('/login');
            return;
        }

        const fetchHistory = async () => {
            try {
                const response = await fetch('http://localhost:5000/api/v1/predict/history', {
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                    },
                });

                if (!response.ok) {
                    if (response.status === 429) {
                        throw new Error('Rate limit exceeded. Please try again in a moment.');
                    }
                    throw new Error('Failed to fetch history');
                }

                const data = await response.json();
                if (isMounted) setHistory(data.history || []);
            } catch (err: any) {
                if (isMounted) setError(err.message || 'An error occurred while fetching history.');
            } finally {
                if (isMounted) setLoading(false);
            }
        };

        fetchHistory();
        return () => { isMounted = false; };
    }, [accessToken, isAuthenticated, navigate]);

    const getRiskColor = (level: string) => {
        switch (level.toLowerCase()) {
            case 'high': return '#D32F2F';
            case 'medium': return '#ED6C02';
            case 'low': return '#2E7D32';
            default: return '#1976D2';
        }
    };

    const stats = [
        { label: 'Total Scans', value: history.length, icon: <BarChartIcon />, color: '#452829' },
        { label: 'Latest Check', value: history.length > 0 ? new Date(history[0].created_at).toLocaleDateString() : 'N/A', icon: <CalendarTodayIcon />, color: '#E8D1C5' },
        { label: 'Security Level', value: 'High', icon: <HealthAndSafetyIcon />, color: '#2E7D32' }
    ];

    if (loading) {
        return (
            <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: '#F3E8DF' }}>
                <CircularProgress sx={{ color: '#452829' }} />
            </Box>
        );
    }

    return (
        <Box sx={{ minHeight: '100vh', pt: { xs: 8, md: 12 }, pb: 8, bgcolor: '#F3E8DF' }}>
            <Container maxWidth="lg">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <Box sx={{ mb: 6 }}>
                        <Typography variant="h3" sx={{ fontWeight: 900, mb: 1, fontFamily: "'Outfit', sans-serif" }}>
                            Diagnostic <span style={{ color: '#C5A898' }}>Vault.</span>
                        </Typography>
                        <Typography variant="body1" sx={{ color: 'text.secondary', fontWeight: 500 }}>
                            Review your past AI health assessments and track changes over time.
                        </Typography>
                    </Box>

                    {/* Stats Summary Bar */}
                    <Grid container spacing={3} sx={{ mb: 6 }}>
                        {stats.map((stat, i) => (
                            <Grid item xs={12} sm={4} key={i}>
                                <Paper
                                    elevation={0}
                                    sx={{
                                        p: 3,
                                        borderRadius: '24px',
                                        bgcolor: 'white',
                                        border: '1px solid rgba(0,0,0,0.03)',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: 2,
                                        boxShadow: '0 10px 20px rgba(69, 40, 41, 0.03)'
                                    }}
                                >
                                    <Avatar sx={{ bgcolor: '#F8F4F1', color: stat.color, width: 48, height: 48 }}>
                                        {stat.icon}
                                    </Avatar>
                                    <Box>
                                        <Typography variant="h5" sx={{ fontWeight: 900, lineHeight: 1.2 }}>{stat.value}</Typography>
                                        <Typography variant="caption" sx={{ color: 'text.secondary', fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5 }}>{stat.label}</Typography>
                                    </Box>
                                </Paper>
                            </Grid>
                        ))}
                    </Grid>

                    {error && (
                        <Alert severity="error" sx={{ mb: 4, borderRadius: '16px' }}>
                            {error}
                        </Alert>
                    )}

                    {history.length === 0 ? (
                        <Paper
                            elevation={0}
                            sx={{
                                p: 10,
                                textAlign: 'center',
                                borderRadius: '40px',
                                bgcolor: 'white',
                                border: '1px solid rgba(0,0,0,0.05)'
                            }}
                        >
                            <Box sx={{
                                display: 'inline-flex',
                                p: 3,
                                borderRadius: '50%',
                                bgcolor: '#F8F4F1',
                                mb: 3,
                                color: '#452829'
                            }}>
                                <AssessmentIcon sx={{ fontSize: 48 }} />
                            </Box>
                            <Typography variant="h4" sx={{ fontWeight: 900, mb: 2 }}>No Records Found.</Typography>
                            <Typography variant="body1" color="text.secondary" sx={{ mb: 4, maxWidth: 400, mx: 'auto' }}>
                                Your diagnostic history is empty. Start a new AI analysis to build your clinical profile.
                            </Typography>
                            <Button
                                variant="contained"
                                size="large"
                                onClick={() => navigate('/analyze')}
                                sx={{
                                    bgcolor: '#2D1B1C',
                                    color: 'white',
                                    px: 6,
                                    py: 2,
                                    borderRadius: '16px',
                                    fontWeight: 900,
                                    '&:hover': { bgcolor: '#000' }
                                }}
                            >
                                Start First Analysis
                            </Button>
                        </Paper>
                    ) : (
                        <Grid container spacing={3}>
                            <AnimatePresence>
                                {history.map((item, index) => (
                                    <Grid item xs={12} key={item.analysis_id}>
                                        <motion.div
                                            initial={{ opacity: 0, x: -20 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            transition={{ duration: 0.4, delay: index * 0.1 }}
                                        >
                                            <Card
                                                elevation={0}
                                                sx={{
                                                    borderRadius: '24px',
                                                    cursor: 'pointer',
                                                    border: '1px solid rgba(0,0,0,0.03)',
                                                    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                                                    '&:hover': {
                                                        transform: 'scale(1.01)',
                                                        boxShadow: '0 30px 60px rgba(69, 40, 41, 0.08)',
                                                        bgcolor: 'white'
                                                    },
                                                    bgcolor: 'rgba(255,255,255,0.7)'
                                                }}
                                                onClick={() => navigate(`/results/${item.analysis_id}`, { state: { result: item } })}
                                            >
                                                <CardContent sx={{ display: 'flex', alignItems: 'center', p: 4, '&:last-child': { pb: 4 } }}>
                                                    <Box sx={{
                                                        mr: 4,
                                                        p: 2,
                                                        borderRadius: '16px',
                                                        bgcolor: '#2D1B1C',
                                                        color: '#E8D1C5',
                                                        display: { xs: 'none', sm: 'flex' }
                                                    }}>
                                                        <BiotechIcon />
                                                    </Box>
                                                    <Box sx={{ flexGrow: 1 }}>
                                                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                                                            <Typography variant="h5" sx={{ fontWeight: 900, color: '#2D1B1C' }}>
                                                                {item.prediction}
                                                            </Typography>
                                                            <Chip
                                                                label={`${item.risk} Risk`}
                                                                size="small"
                                                                sx={{
                                                                    height: 24,
                                                                    fontSize: '0.75rem',
                                                                    fontWeight: 800,
                                                                    color: 'white',
                                                                    bgcolor: getRiskColor(item.risk),
                                                                    px: 1,
                                                                    borderRadius: '6px'
                                                                }}
                                                            />
                                                        </Box>
                                                        <Stack direction="row" spacing={3} alignItems="center">
                                                            <Typography variant="body2" sx={{ color: 'text.secondary', fontWeight: 600, display: 'flex', alignItems: 'center', gap: 1 }}>
                                                                <CalendarTodayIcon sx={{ fontSize: '1rem' }} />
                                                                {new Date(item.created_at).toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' })}
                                                            </Typography>
                                                            <Typography variant="body2" sx={{ color: 'text.disabled', fontWeight: 600 }}>
                                                                ID: {item.analysis_id.slice(0, 8)}...
                                                            </Typography>
                                                        </Stack>
                                                    </Box>
                                                    <IconButton sx={{ bgcolor: '#F8F4F1', '&:hover': { bgcolor: '#E8D1C5' } }}>
                                                        <ChevronRightIcon />
                                                    </IconButton>
                                                </CardContent>
                                            </Card>
                                        </motion.div>
                                    </Grid>
                                ))}
                            </AnimatePresence>
                        </Grid>
                    )}
                </motion.div>
            </Container>
        </Box>
    );
};

export default HistoryPage;
