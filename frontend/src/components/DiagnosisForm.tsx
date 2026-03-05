import React, { useState } from 'react';
import axios from 'axios';
import {
    Box,
    Typography,
    TextField,
    Button,
    CircularProgress,
    Paper,
    Chip,
    Fade,
    List,
    ListItem,
    ListItemText,
    Divider
} from '@mui/material';
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety';
import SendIcon from '@mui/icons-material/Send';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';

export const DiagnosisForm = () => {
    const [symptoms, setSymptoms] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [error, setError] = useState('');

    const handlePredict = async () => {
        if (!symptoms.trim()) {
            setError('Please enter some symptoms.');
            return;
        }
        setError('');
        setLoading(true);
        setResult(null);

        try {
            // Use environment variable for API URL in production
            const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/v1/predict/analyze`, {
                symptoms: symptoms
            });
            setResult(response.data);
        } catch (err: any) {
            console.error(err);
            setError('An error occurred while analyzing symptoms. Is the backend running?');
        } finally {
            setLoading(false);
        }
    };

    const getRiskColor = (risk: string) => {
        switch (risk?.toLowerCase()) {
            case 'high': return 'error';
            case 'medium': return 'warning';
            case 'low': return 'success';
            default: return 'default';
        }
    };

    return (
        <Box sx={{ maxWidth: 800, margin: '0 auto', p: 2 }}>
            <Paper
                elevation={24}
                sx={{
                    p: 4,
                    borderRadius: 4,
                    background: 'rgba(25, 30, 40, 0.7)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255,255,255,0.1)',
                    color: 'white'
                }}
            >
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3, gap: 2 }}>
                    <HealthAndSafetyIcon sx={{ fontSize: 40, color: '#4dabf5' }} />
                    <Typography variant="h4" fontWeight={700}>
                        AI Symptom Analyzer
                    </Typography>
                </Box>

                <Typography variant="body1" sx={{ mb: 4, color: 'rgba(255,255,255,0.7)' }}>
                    Describe your symptoms in detail. Advanced ML models will compute the topmost probable conditions and recommend a medical specialist for you to consult.
                </Typography>

                <TextField
                    fullWidth
                    multiline
                    rows={4}
                    variant="outlined"
                    placeholder="e.g. I have a severe headache, skin rash, and high fever for 3 days..."
                    value={symptoms}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSymptoms(e.target.value)}
                    sx={{
                        mb: 3,
                        '& .MuiOutlinedInput-root': {
                            color: 'white',
                            backgroundColor: 'rgba(0,0,0,0.2)',
                            '& fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
                            '&:hover fieldset': { borderColor: '#4dabf5' },
                            '&.Mui-focused fieldset': { borderColor: '#4dabf5' },
                        }
                    }}
                />

                {error && (
                    <Typography color="error" sx={{ mb: 2 }}>{error}</Typography>
                )}

                <Button
                    variant="contained"
                    size="large"
                    color="primary"
                    endIcon={loading ? <CircularProgress size={20} color="inherit" /> : <SendIcon />}
                    onClick={handlePredict}
                    disabled={loading}
                    sx={{
                        px: 4,
                        py: 1.5,
                        borderRadius: 8,
                        textTransform: 'none',
                        fontSize: '1.1rem',
                        background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                        boxShadow: '0 3px 15px 2px rgba(33, 203, 243, .3)',
                    }}
                >
                    {loading ? 'Analyzing...' : 'Analyze Symptoms'}
                </Button>
            </Paper>

            <Fade in={!!result}>
                <Box sx={{ mt: 4 }}>
                    {result && (
                        <Paper
                            elevation={24}
                            sx={{
                                p: 4,
                                borderRadius: 4,
                                background: 'rgba(255, 255, 255, 0.05)',
                                backdropFilter: 'blur(10px)',
                                border: '1px solid rgba(255,255,255,0.1)',
                                color: 'white'
                            }}
                        >
                            <Typography variant="h5" fontWeight={600} gutterBottom>
                                Analysis Results
                            </Typography>

                            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', my: 3 }}>
                                <Chip
                                    icon={<WarningAmberIcon />}
                                    label={`Risk Level: ${result.risk}`}
                                    color={getRiskColor(result.risk) as any}
                                    sx={{ fontSize: '1.1rem', py: 2.5, px: 1 }}
                                />
                                <Chip
                                    label={`Recommended Specialist: ${result.doctor}`}
                                    color="info"
                                    variant="outlined"
                                    sx={{ fontSize: '1.1rem', py: 2.5, px: 1, color: '#4dabf5', borderColor: '#4dabf5' }}
                                />
                            </Box>

                            <Typography variant="h6" sx={{ mt: 4, mb: 2, color: '#21CBF3' }}>
                                Top Matches
                            </Typography>
                            <List sx={{ bgcolor: 'rgba(0,0,0,0.2)', borderRadius: 2 }}>
                                {(result.top_diseases || []).map((diseaseInfo: any, idx: number) => (
                                    <React.Fragment key={idx}>
                                        <ListItem>
                                            <ListItemText
                                                primary={
                                                    <Typography variant="h6">{diseaseInfo.disease}</Typography>
                                                }
                                                secondary={
                                                    <Typography sx={{ color: 'rgba(255,255,255,0.6)' }}>
                                                        Probability: {diseaseInfo.probability}%
                                                    </Typography>
                                                }
                                            />
                                            <CircularProgress
                                                variant="determinate"
                                                value={diseaseInfo.probability}
                                                color={idx === 0 ? 'success' : 'primary'}
                                                size={50}
                                                thickness={4}
                                            />
                                        </ListItem>
                                        {idx < result.top_diseases.length - 1 && <Divider sx={{ borderColor: 'rgba(255,255,255,0.1)' }} />}
                                    </React.Fragment>
                                ))}
                            </List>

                            {result.matched_symptoms && result.matched_symptoms.length > 0 && (
                                <>
                                    <Typography variant="subtitle1" sx={{ mt: 4, mb: 1, color: 'rgba(255,255,255,0.6)' }}>
                                        Symptoms Detected:
                                    </Typography>
                                    <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                                        {result.matched_symptoms.map((sym: string, idx: number) => (
                                            <Chip key={idx} label={sym} size="small" sx={{ bgcolor: 'rgba(255,255,255,0.1)', color: 'white' }} />
                                        ))}
                                    </Box>
                                </>
                            )}
                        </Paper>
                    )}
                </Box>
            </Fade>
        </Box>
    );
};
