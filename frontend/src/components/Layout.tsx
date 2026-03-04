import React, { ReactNode, useState } from 'react';
import { Box, AppBar, Toolbar, Typography, Button, Container, IconButton, Menu, MenuItem, Avatar, Link as MuiLink, useScrollTrigger } from '@mui/material';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import HistoryIcon from '@mui/icons-material/History';
import LogoutIcon from '@mui/icons-material/Logout';
import Grid from '@mui/material/Grid';
import { motion, AnimatePresence } from 'framer-motion';

interface LayoutProps {
    children: ReactNode;
}

const ElevationScroll = (props: { children: React.ReactElement }) => {
    const { children } = props;
    const trigger = useScrollTrigger({
        disableHysteresis: true,
        threshold: 20,
    });

    return React.cloneElement(children, {
        elevation: 0,
        sx: {
            backgroundColor: trigger ? 'rgba(45, 27, 28, 0.95)' : 'transparent',
            backdropFilter: trigger ? 'blur(16px)' : 'none',
            transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
            borderBottom: trigger ? '1px solid rgba(232, 209, 197, 0.1)' : 'none',
            py: trigger ? 0 : 0.5,
        }
    });
};

const Layout = ({ children }: LayoutProps) => {
    const { user, isAuthenticated, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

    const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleLogout = () => {
        logout();
        handleClose();
        navigate('/');
    };

    const navItems = [
        { label: 'Home', path: '/' },
        { label: 'Analyze', path: '/analyze' },
        { label: 'History', path: '/history' },
    ];

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', bgcolor: '#F3E8DF' }}>
            <ElevationScroll>
                <AppBar position="fixed" sx={{ bgcolor: 'transparent', boxShadow: 'none' }}>
                    <Container maxWidth="lg">
                        <Toolbar disableGutters sx={{ minHeight: { xs: 64, md: 72 } }}>
                            <Box
                                component={Link}
                                to="/"
                                sx={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    textDecoration: 'none',
                                    color: 'white',
                                    flexGrow: 1
                                }}
                            >
                                <motion.div
                                    whileHover={{ rotate: 5 }}
                                    transition={{ type: "spring", stiffness: 400, damping: 10 }}
                                >
                                    <Box sx={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        bgcolor: 'rgba(232, 209, 197, 0.2)',
                                        p: 0.8,
                                        borderRadius: '10px',
                                        mr: 1.2,
                                    }}>
                                        <LocalHospitalIcon sx={{ fontSize: 24, color: '#E8D1C5' }} />
                                    </Box>
                                </motion.div>
                                <Typography
                                    variant="h6"
                                    sx={{
                                        fontWeight: 900,
                                        letterSpacing: '-0.5px',
                                        fontFamily: "'Outfit', sans-serif",
                                        color: 'white',
                                        fontSize: { xs: '1.1rem', sm: '1.3rem' }
                                    }}
                                >
                                    MediDiagnose <span style={{ color: '#E8D1C5' }}>AI</span>
                                </Typography>
                            </Box>

                            <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 1, mr: 4 }}>
                                {navItems.map((item) => (
                                    <Button
                                        key={item.label}
                                        component={Link}
                                        to={item.path}
                                        sx={{
                                            color: location.pathname === item.path ? '#E8D1C5' : 'rgba(255,255,255,0.8)',
                                            fontWeight: 700,
                                            fontSize: '0.875rem',
                                            textTransform: 'none',
                                            px: 2,
                                            '&:hover': {
                                                color: 'white',
                                                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                                            },
                                        }}
                                    >
                                        {item.label}
                                    </Button>
                                ))}
                            </Box>

                            {isAuthenticated ? (
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                                    <IconButton
                                        onClick={handleMenu}
                                        sx={{
                                            p: 0,
                                            border: '2px solid rgba(232, 209, 197, 0.3)',
                                            transition: '0.3s',
                                            '&:hover': { borderColor: '#E8D1C5' }
                                        }}
                                    >
                                        <Avatar sx={{
                                            bgcolor: '#E8D1C5',
                                            color: '#452829',
                                            width: 36,
                                            height: 36,
                                            fontWeight: 800,
                                            fontSize: '0.9rem'
                                        }}>
                                            {user?.email[0].toUpperCase()}
                                        </Avatar>
                                    </IconButton>
                                    <Menu
                                        anchorEl={anchorEl}
                                        open={Boolean(anchorEl)}
                                        onClose={handleClose}
                                        disableScrollLock
                                        PaperProps={{
                                            className: 'glass-panel',
                                            sx: { mt: 1.5, minWidth: 200, borderRadius: 2, p: 1, bgcolor: 'white' }
                                        }}
                                        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
                                        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
                                    >
                                        <MenuItem onClick={() => { navigate('/profile'); handleClose(); }} sx={{ borderRadius: 1.5, py: 1 }}>
                                            <AccountCircleIcon sx={{ mr: 1.5, color: '#452829', fontSize: 20 }} />
                                            <Typography variant="body2" sx={{ fontWeight: 600 }}>Profile</Typography>
                                        </MenuItem>
                                        <MenuItem onClick={() => { navigate('/history'); handleClose(); }} sx={{ borderRadius: 1.5, py: 1 }}>
                                            <HistoryIcon sx={{ mr: 1.5, color: '#452829', fontSize: 20 }} />
                                            <Typography variant="body2" sx={{ fontWeight: 600 }}>History</Typography>
                                        </MenuItem>
                                        <Box sx={{ my: 1, borderTop: '1px solid rgba(0,0,0,0.06)' }} />
                                        <MenuItem onClick={handleLogout} sx={{ borderRadius: 1.5, py: 1, color: '#d32f2f' }}>
                                            <LogoutIcon sx={{ mr: 1.5, fontSize: 20 }} />
                                            <Typography variant="body2" sx={{ fontWeight: 700 }}>Logout</Typography>
                                        </MenuItem>
                                    </Menu>
                                </Box>
                            ) : (
                                <Box sx={{ display: 'flex', gap: 1.5 }}>
                                    <Button
                                        component={Link}
                                        to="/login"
                                        sx={{
                                            color: 'white',
                                            fontWeight: 700,
                                            textTransform: 'none',
                                            fontSize: '0.875rem'
                                        }}
                                    >
                                        Log in
                                    </Button>
                                    <Button
                                        variant="contained"
                                        component={Link}
                                        to="/register"
                                        sx={{
                                            bgcolor: '#E8D1C5',
                                            color: '#452829',
                                            fontWeight: 800,
                                            px: 2.5,
                                            py: 0.8,
                                            borderRadius: '8px',
                                            textTransform: 'none',
                                            fontSize: '0.875rem',
                                            '&:hover': { bgcolor: '#FFF' }
                                        }}
                                    >
                                        Sign up
                                    </Button>
                                </Box>
                            )}
                        </Toolbar>
                    </Container>
                </AppBar>
            </ElevationScroll>

            <AnimatePresence mode="wait">
                <motion.main
                    key={location.pathname}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    style={{ flexGrow: 1 }}
                >
                    {children}
                </motion.main>
            </AnimatePresence>

            <Box
                component="footer"
                sx={{
                    bgcolor: '#1A1112',
                    color: 'white',
                    pt: 8,
                    pb: 4,
                }}
            >
                <Container maxWidth="lg">
                    <Grid container spacing={4}>
                        <Grid item xs={12} md={4}>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                                <LocalHospitalIcon sx={{ color: '#E8D1C5', mr: 1.5 }} />
                                <Typography variant="h6" sx={{ fontWeight: 900, fontFamily: "'Outfit', sans-serif" }}>
                                    MediDiagnose AI
                                </Typography>
                            </Box>
                            <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.5)', lineHeight: 1.7, maxWidth: 280 }}>
                                Professional AI-driven preliminary health assessments. Secure, private, and precise.
                            </Typography>
                        </Grid>

                        <Grid item xs={6} md={2}>
                            <Typography variant="subtitle2" sx={{ fontWeight: 800, mb: 2, color: '#E8D1C5' }}>Platform</Typography>
                            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                                {[
                                    { label: 'Analyze Health', path: '/analyze' },
                                    { label: 'View History', path: '/history' },
                                    { label: 'My Profile', path: '/profile' },
                                    { label: 'Dashboard', path: '/' },
                                ].map(item => (
                                    <MuiLink key={item.label} component={Link} to={item.path} sx={{ color: 'rgba(255,255,255,0.4)', textDecoration: 'none', fontSize: '0.8rem', '&:hover': { color: 'white' } }}>
                                        {item.label}
                                    </MuiLink>
                                ))}
                            </Box>
                        </Grid>

                        <Grid item xs={6} md={2}>
                            <Typography variant="subtitle2" sx={{ fontWeight: 800, mb: 2, color: '#E8D1C5' }}>Account</Typography>
                            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                                {[
                                    { label: 'Log In', path: '/login' },
                                    { label: 'Sign Up', path: '/register' },
                                    { label: 'Privacy Policy', path: '/privacy' },
                                    { label: 'Terms of Service', path: '/terms' },
                                ].map(item => (
                                    <MuiLink key={item.label} component={Link} to={item.path} sx={{ color: 'rgba(255,255,255,0.4)', textDecoration: 'none', fontSize: '0.8rem', '&:hover': { color: 'white' } }}>
                                        {item.label}
                                    </MuiLink>
                                ))}
                            </Box>
                        </Grid>

                        <Grid item xs={12} md={4}>
                            <Typography variant="subtitle2" sx={{ fontWeight: 800, mb: 2, color: 'white' }}>Newsletter</Typography>
                            <Box sx={{ display: 'flex', gap: 1 }}>
                                <Box
                                    component="input"
                                    placeholder="your@email.com"
                                    sx={{
                                        p: 1.2,
                                        borderRadius: '8px',
                                        border: '1px solid rgba(255,255,255,0.1)',
                                        bgcolor: 'rgba(255,255,255,0.05)',
                                        color: 'white',
                                        flexGrow: 1,
                                        fontSize: '0.85rem',
                                        '&:focus': { outline: 'none', borderColor: '#E8D1C5' }
                                    }}
                                />
                                <Button variant="contained" size="small" sx={{ bgcolor: '#E8D1C5', color: '#452829', fontWeight: 800, borderRadius: '8px' }}>Join</Button>
                            </Box>
                        </Grid>
                    </Grid>

                    <Box sx={{ mt: 8, pt: 3, borderTop: '1px solid rgba(255, 255, 255, 0.05)', textAlign: 'center' }}>
                        <Typography variant="caption" sx={{ color: 'rgba(255, 255, 255, 0.3)' }}>
                            © 2026 MEDIDIAGNOSE AI • PRECISION AI HEALTHCARE
                        </Typography>
                    </Box>
                </Container>
            </Box>
        </Box>
    );
};

export default Layout;
