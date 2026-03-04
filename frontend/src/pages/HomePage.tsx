import { Container, Typography, Button, Box, Grid, Paper, Stack, Avatar } from '@mui/material';
import { motion, useScroll, useTransform, Variants, TargetAndTransition } from 'framer-motion';
import { Link } from 'react-router-dom';
import SecurityIcon from '@mui/icons-material/Security';
import SpeedIcon from '@mui/icons-material/Speed';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import BiotechIcon from '@mui/icons-material/Biotech';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import AssignmentIcon from '@mui/icons-material/Assignment';
import BarChartIcon from '@mui/icons-material/BarChart';
import ShieldIcon from '@mui/icons-material/Shield';

// Variants for staggered animations
const containerVariants: Variants = {
    initial: {},
    animate: {
        transition: {
            staggerChildren: 0.2,
        },
    },
};

const itemVariants: Variants = {
    initial: { opacity: 0, y: 20 },
    animate: {
        opacity: 1,
        y: 0,
        transition: {
            duration: 0.8,
            ease: [0.6, 0.05, 0.01, 0.9],
        },
    } as TargetAndTransition,
};

const floatingVariants: Variants = {
    animate: {
        y: [0, -15, 0],
        transition: {
            duration: 4,
            repeat: Infinity,
            ease: "easeInOut"
        } as any
    }
};

const HomePage = () => {
    const { scrollY } = useScroll();
    const yParallax = useTransform(scrollY, [0, 500], [0, 150]);

    const features = [
        {
            icon: <BiotechIcon sx={{ fontSize: 24, color: '#E8D1C5' }} />,
            title: 'Neural Engine',
            description: 'Advanced AI models trained for clinical analysis.'
        },
        {
            icon: <SecurityIcon sx={{ fontSize: 24, color: '#E8D1C5' }} />,
            title: 'Private by Design',
            description: 'Your data never leaves our secure encrypted tunnel.'
        },
        {
            icon: <SpeedIcon sx={{ fontSize: 24, color: '#E8D1C5' }} />,
            title: 'Instant Results',
            description: 'Preliminary health assessments in under 10 seconds.'
        }
    ];

    const steps = [
        {
            number: '01',
            title: 'Input Symptoms',
            description: 'Describe what you\'re feeling using our intuitive symptom selector.'
        },
        {
            number: '02',
            title: 'Neural Processing',
            description: 'Our AI analyzes patterns across thousands of clinical data points.'
        },
        {
            number: '03',
            title: 'Dynamic Report',
            description: 'Receive a prioritized list of possibilities and suggested next steps.'
        }
    ];

    return (
        <Box sx={{ overflowX: 'hidden', bgcolor: '#F3E8DF' }}>
            {/* Hero Section */}
            <Box
                sx={{
                    position: 'relative',
                    height: '100vh',
                    width: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    background: '#1A1112',
                    pt: { xs: 15, md: 10 },
                    color: 'white',
                    overflow: 'hidden',
                }}
            >
                {/* High-End Background Image with Parallax */}
                <motion.div
                    style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        y: yParallax,
                        backgroundImage: 'url("https://images.unsplash.com/photo-1551076805-e1869033e561?auto=format&fit=crop&q=80&w=2670")',
                        backgroundPosition: 'center',
                        backgroundSize: 'cover',
                        zIndex: 0,
                    }}
                >
                    <Box
                        sx={{
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            right: 0,
                            bottom: 0,
                            background: {
                                xs: 'linear-gradient(to bottom, rgba(26, 17, 18, 0.95), rgba(26, 17, 18, 0.8))',
                                md: 'linear-gradient(to right, rgba(26, 17, 18, 1) 0%, rgba(26, 17, 18, 0.6) 50%, rgba(26, 17, 18, 0.2) 100%)'
                            },
                        }}
                    />
                </motion.div>

                {/* Floating Glassmorphism Elements */}
                <Box sx={{ position: 'absolute', top: '20%', right: '15%', display: { xs: 'none', lg: 'block' }, zIndex: 1 }}>
                    <motion.div variants={floatingVariants} animate="animate">
                        <Paper sx={{
                            p: 3,
                            borderRadius: '24px',
                            bgcolor: 'rgba(255, 255, 255, 0.05)',
                            backdropFilter: 'blur(20px)',
                            border: '1px solid rgba(255, 255, 255, 0.1)',
                            boxShadow: '0 20px 40px rgba(0,0,0,0.3)'
                        }}>
                            <Stack direction="row" spacing={2} alignItems="center">
                                <Avatar sx={{ bgcolor: '#E8D1C5', width: 40, height: 40 }}>
                                    <BiotechIcon sx={{ color: '#452829' }} />
                                </Avatar>
                                <Box>
                                    <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)', fontWeight: 700 }}>AI STATUS</Typography>
                                    <Typography variant="body2" sx={{ color: 'white', fontWeight: 800 }}>Analyzing Symptoms...</Typography>
                                </Box>
                            </Stack>
                        </Paper>
                    </motion.div>
                </Box>

                <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 2 }}>
                    <Grid container spacing={4} alignItems="center">
                        <Grid item xs={12} md={7}>
                            <motion.div
                                variants={containerVariants}
                                initial="initial"
                                animate="animate"
                            >
                                <motion.div variants={itemVariants}>
                                    <Box sx={{
                                        display: 'inline-flex',
                                        bgcolor: 'rgba(232, 209, 197, 0.15)',
                                        px: 2,
                                        py: 0.5,
                                        borderRadius: '50px',
                                        mb: 3,
                                        border: '1px solid rgba(232, 209, 197, 0.2)'
                                    }}>
                                        <Typography variant="caption" sx={{ color: '#E8D1C5', fontWeight: 900, letterSpacing: '1px' }}>
                                            AI-POWERED DIAGNOSTICS
                                        </Typography>
                                    </Box>
                                </motion.div>

                                <motion.div variants={itemVariants}>
                                    <Typography variant="h1" sx={{
                                        fontSize: { xs: '2.5rem', md: '4rem' },
                                        fontWeight: 900,
                                        lineHeight: 1,
                                        mb: 3,
                                        fontFamily: "'Outfit', sans-serif",
                                        letterSpacing: '-2px',
                                        color: 'white'
                                    }}>
                                        The Future of <br />
                                        <span style={{
                                            background: 'linear-gradient(135deg, #E8D1C5 0%, #FFF 100%)',
                                            WebkitBackgroundClip: 'text',
                                            WebkitTextFillColor: 'transparent',
                                        }}>
                                            AI Diagnosis.
                                        </span>
                                    </Typography>
                                </motion.div>

                                <motion.div variants={itemVariants}>
                                    <Typography variant="h6" sx={{
                                        color: 'rgba(255, 255, 255, 0.7)',
                                        mb: 5,
                                        lineHeight: 1.6,
                                        maxWidth: '540px',
                                        fontWeight: 400
                                    }}>
                                        Access medical-grade preliminary analysis from anywhere. Experience a secure, AI-powered health assistant that understands you.
                                    </Typography>
                                </motion.div>

                                <motion.div variants={itemVariants}>
                                    <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2.5}>
                                        <Button
                                            variant="contained"
                                            component={Link}
                                            to="/analyze"
                                            sx={{
                                                bgcolor: '#E8D1C5',
                                                color: '#452829',
                                                px: 4,
                                                py: 1.5,
                                                borderRadius: '10px',
                                                fontWeight: 900,
                                                fontSize: '0.95rem',
                                                textTransform: 'none',
                                                boxShadow: '0 20px 40px rgba(0,0,0,0.3)',
                                                '&:hover': { bgcolor: '#FFF', transform: 'translateY(-3px)' },
                                                transition: '0.4s cubic-bezier(0.4, 0, 0.2, 1)'
                                            }}
                                            startIcon={<PlayArrowIcon />}
                                        >
                                            Iniate Diagnosis
                                        </Button>
                                        <Button
                                            variant="outlined"
                                            onClick={() => document.getElementById('how-it-works')?.scrollIntoView({ behavior: 'smooth' })}
                                            sx={{
                                                borderColor: 'rgba(255,255,255,0.2)',
                                                color: 'white',
                                                px: 4,
                                                py: 1.5,
                                                borderRadius: '10px',
                                                fontWeight: 700,
                                                textTransform: 'none',
                                                '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.05)' }
                                            }}
                                        >
                                            View Methodology
                                        </Button>
                                    </Stack>
                                </motion.div>
                            </motion.div>
                        </Grid>
                    </Grid>
                </Container>

                <Box sx={{ position: 'absolute', bottom: 40, left: '50%', transform: 'translateX(-50%)', zIndex: 10 }}>
                    <motion.div animate={{ y: [0, 10, 0] }} transition={{ duration: 2, repeat: Infinity }}>
                        <KeyboardArrowDownIcon sx={{ color: 'rgba(255,255,255,0.3)', fontSize: 40 }} />
                    </motion.div>
                </Box>
            </Box>

            {/* Stats Bar */}
            <Box sx={{ bgcolor: 'white', borderBottom: '1px solid rgba(0,0,0,0.05)' }}>
                <Container maxWidth="lg">
                    <Grid container sx={{ py: 6 }} spacing={4} justifyContent="center">
                        {[
                            { label: 'Accuracy Rate', value: '98.4%', icon: <BarChartIcon /> },
                            { label: 'Analysis Processed', value: '1.2M+', icon: <AssignmentIcon /> },
                            { label: 'Secure Encryption', value: 'AES-256', icon: <ShieldIcon /> },
                        ].map((stat, i) => (
                            <Grid item xs={12} sm={4} key={i}>
                                <Stack direction="row" spacing={2} alignItems="center" justifyContent="center">
                                    <Box sx={{ color: '#452829', bgcolor: '#F3E8DF', p: 1.5, borderRadius: '12px' }}>
                                        {stat.icon}
                                    </Box>
                                    <Box>
                                        <Typography variant="h5" sx={{ fontWeight: 900, color: '#452829' }}>{stat.value}</Typography>
                                        <Typography variant="caption" sx={{ color: 'text.secondary', fontWeight: 600 }}>{stat.label}</Typography>
                                    </Box>
                                </Stack>
                            </Grid>
                        ))}
                    </Grid>
                </Container>
            </Box>

            {/* Features Section */}
            <Box sx={{ py: 15, position: 'relative' }}>
                <Container maxWidth="lg">
                    <Box sx={{ textAlign: 'center', mb: 10 }}>
                        <Typography variant="overline" sx={{ color: '#452829', fontWeight: 900, letterSpacing: 2 }}>CORE CAPABILITIES</Typography>
                        <Typography variant="h2" sx={{ fontWeight: 900, fontFamily: "'Outfit', sans-serif", mt: 1 }}>Unmatched Precision.</Typography>
                    </Box>
                    <Grid container spacing={4}>
                        {features.map((feature, index) => (
                            <Grid item xs={12} md={4} key={index}>
                                <motion.div
                                    initial={{ opacity: 0, y: 40 }}
                                    whileInView={{ opacity: 1, y: 0 }}
                                    viewport={{ once: true }}
                                    transition={{ duration: 0.6, delay: index * 0.2 }}
                                >
                                    <Paper
                                        elevation={0}
                                        sx={{
                                            p: 4,
                                            height: '100%',
                                            borderRadius: '24px',
                                            bgcolor: 'white',
                                            border: '1px solid rgba(0,0,0,0.03)',
                                            boxShadow: '0 30px 60px rgba(69, 40, 41, 0.05)',
                                            '&:hover': { transform: 'translateY(-5px)', boxShadow: '0 40px 80px rgba(69, 40, 41, 0.08)' },
                                            transition: '0.4s cubic-bezier(0.4, 0, 0.2, 1)'
                                        }}
                                    >
                                        <Box sx={{
                                            display: 'flex',
                                            p: 1.5,
                                            borderRadius: '16px',
                                            bgcolor: '#2D1B1C',
                                            mb: 3,
                                            width: 'fit-content'
                                        }}>
                                            {feature.icon}
                                        </Box>
                                        <Typography variant="h6" sx={{ mb: 1.5, fontWeight: 900, fontFamily: "'Outfit', sans-serif" }}>{feature.title}</Typography>
                                        <Typography variant="body2" sx={{ color: 'rgba(0,0,0,0.5)', lineHeight: 1.6 }}>
                                            {feature.description}
                                        </Typography>
                                    </Paper>
                                </motion.div>
                            </Grid>
                        ))}
                    </Grid>
                </Container>
            </Box>

            {/* How It Works Section */}
            <Box id="how-it-works" sx={{ py: 15, bgcolor: '#FAF5F2' }}>
                <Container maxWidth="lg">
                    <Grid container spacing={8} alignItems="center">
                        <Grid item xs={12} md={5}>
                            <Typography variant="overline" sx={{ color: '#452829', fontWeight: 900, letterSpacing: 2 }}>PROCESS FLOW</Typography>
                            <Typography variant="h2" sx={{ fontWeight: 900, fontFamily: "'Outfit', sans-serif", mt: 1, mb: 3 }}>How it Works.</Typography>
                            <Typography variant="body1" sx={{ color: 'text.secondary', mb: 4, lineHeight: 1.8 }}>
                                Leveraging the latest breakthroughs in large language models and biomedical encoding, our platform provides a seamless 3-step path to health insights.
                            </Typography>
                            <Button
                                variant="contained"
                                sx={{ bgcolor: '#452829', color: 'white', px: 4, py: 1.5, borderRadius: '10px', '&:hover': { bgcolor: '#000' } }}
                                component={Link}
                                to="/register"
                            >
                                Start Your Journey
                            </Button>
                        </Grid>
                        <Grid item xs={12} md={7}>
                            <Stack spacing={4}>
                                {steps.map((step, i) => (
                                    <motion.div
                                        key={i}
                                        initial={{ opacity: 0, x: 50 }}
                                        whileInView={{ opacity: 1, x: 0 }}
                                        viewport={{ once: true }}
                                        transition={{ duration: 0.6, delay: i * 0.1 }}
                                    >
                                        <Paper
                                            elevation={0}
                                            sx={{
                                                p: 3,
                                                borderRadius: '20px',
                                                border: '1px solid rgba(0,0,0,0.05)',
                                                display: 'flex',
                                                gap: 3,
                                                alignItems: 'center',
                                                '&:hover': { bgcolor: 'white', boxShadow: '0 20px 40px rgba(0,0,0,0.05)' },
                                                transition: '0.3s'
                                            }}
                                        >
                                            <Typography variant="h3" sx={{ fontWeight: 900, color: '#E8D1C5', opacity: 0.5 }}>{step.number}</Typography>
                                            <Box>
                                                <Typography variant="h6" sx={{ fontWeight: 900 }}>{step.title}</Typography>
                                                <Typography variant="body2" sx={{ color: 'text.secondary' }}>{step.description}</Typography>
                                            </Box>
                                        </Paper>
                                    </motion.div>
                                ))}
                            </Stack>
                        </Grid>
                    </Grid>
                </Container>
            </Box>

            {/* Security Section */}
            <Box sx={{ py: 15, bgcolor: 'white' }}>
                <Container maxWidth="lg">
                    <Grid container spacing={6} alignItems="center">
                        <Grid item xs={12} md={6}>
                            <motion.div
                                initial={{ opacity: 0, scale: 0.95 }}
                                whileInView={{ opacity: 1, scale: 1 }}
                                viewport={{ once: true }}
                                transition={{ duration: 0.8 }}
                            >
                                <Box sx={{
                                    position: 'relative',
                                    borderRadius: '30px',
                                    overflow: 'hidden',
                                    aspectRatio: '1/1',
                                    backgroundImage: 'url("https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&q=80&w=1470")',
                                    backgroundSize: 'cover'
                                }}>
                                    <Box sx={{
                                        position: 'absolute',
                                        top: 0, left: 0, right: 0, bottom: 0,
                                        bgcolor: 'rgba(69, 40, 41, 0.4)',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center'
                                    }}>
                                        <ShieldIcon sx={{ fontSize: 120, color: 'white', opacity: 0.8 }} />
                                    </Box>
                                </Box>
                            </motion.div>
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <Typography variant="overline" sx={{ color: '#452829', fontWeight: 900, letterSpacing: 2 }}>TRUST & SAFETY</Typography>
                            <Typography variant="h2" sx={{ fontWeight: 900, fontFamily: "'Outfit', sans-serif", mt: 1, mb: 3 }}>Your Privacy is <br /><span style={{ color: '#E8D1C5' }}>Non-Negotiable.</span></Typography>
                            <Typography variant="body1" sx={{ color: 'text.secondary', mb: 4, lineHeight: 1.8 }}>
                                We employ military-grade encryption and strict data anonymization protocols. Your health data is processed in real-time and never sold to third parties. We are committed to maintaining the highest standards of digital health security.
                            </Typography>
                            <Stack spacing={2}>
                                {[
                                    'HIPAA-ready Architecture',
                                    'AES-256 End-to-End Encryption',
                                    'Anonymized Neural Processing',
                                    'Zero Knowledge Data Vaults'
                                ].map((item, i) => (
                                    <Stack key={i} direction="row" spacing={2} alignItems="center">
                                        <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: '#E8D1C5' }} />
                                        <Typography variant="body2" sx={{ fontWeight: 700, color: '#452829' }}>{item}</Typography>
                                    </Stack>
                                ))}
                            </Stack>
                        </Grid>
                    </Grid>
                </Container>
            </Box>

            {/* CTA Section */}
            <Box sx={{ py: 10 }}>
                <Container maxWidth="lg">
                    <Paper
                        elevation={0}
                        sx={{
                            borderRadius: '40px',
                            bgcolor: '#2D1B1C',
                            p: { xs: 4, md: 8 },
                            textAlign: 'center',
                            color: 'white',
                            position: 'relative',
                            overflow: 'hidden',
                            backgroundImage: 'url("https://images.unsplash.com/photo-1576091160550-217359f42f8c?auto=format&fit=crop&q=80&w=2670")',
                            backgroundSize: 'cover',
                            backgroundPosition: 'center'
                        }}
                    >
                        {/* Dark Overlay for Visibility */}
                        <Box sx={{
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            right: 0,
                            bottom: 0,
                            bgcolor: 'rgba(45, 27, 28, 0.85)',
                            zIndex: 0
                        }} />

                        <Box sx={{ position: 'relative', zIndex: 1 }}>
                            <Typography variant="h3" sx={{ fontWeight: 900, mb: 2, fontSize: { xs: '2rem', md: '3rem' }, fontFamily: "'Outfit', sans-serif" }}>
                                Ready to Take Control?
                            </Typography>
                            <Typography variant="body1" sx={{ mb: 4, color: 'rgba(255,255,255,0.7)', maxWidth: 600, mx: 'auto', fontWeight: 400, lineHeight: 1.6 }}>
                                Join our community today and gain access to medical-grade AI analysis in seconds. Precision healthcare is just a click away.
                            </Typography>
                            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} justifyContent="center">
                                <Button
                                    variant="contained"
                                    component={Link}
                                    to="/register"
                                    sx={{
                                        bgcolor: '#E8D1C5',
                                        color: '#452829',
                                        px: 4,
                                        py: 1.5,
                                        borderRadius: '12px',
                                        fontWeight: 900,
                                        fontSize: '1rem',
                                        textTransform: 'none',
                                        '&:hover': { bgcolor: '#FFF', transform: 'translateY(-2px)' },
                                        transition: '0.3s'
                                    }}
                                >
                                    Get Started for Free
                                </Button>
                                <Button
                                    variant="outlined"
                                    component="a"
                                    href="mailto:sales@healthai.dev"
                                    sx={{
                                        borderColor: 'rgba(255,255,255,0.3)',
                                        color: 'white',
                                        px: 4,
                                        py: 1.5,
                                        borderRadius: '12px',
                                        fontWeight: 700,
                                        textTransform: 'none',
                                        '&:hover': { bgcolor: 'rgba(255,255,255,0.05)', borderColor: 'white' }
                                    }}
                                >
                                    Talk to Sales
                                </Button>
                            </Stack>
                        </Box>
                    </Paper>
                </Container>
            </Box>
        </Box>
    );
};

export default HomePage;
