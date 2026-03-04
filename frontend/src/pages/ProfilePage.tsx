import { Container, Box, Typography, Paper, Avatar, Divider, Grid, Chip, Button } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SecurityIcon from '@mui/icons-material/Security';
import EmailIcon from '@mui/icons-material/Email';

const ProfilePage = () => {
    const { user } = useAuth();

    if (!user) return null;

    return (
        <Container maxWidth="md" sx={{ py: 8 }}>
            <Paper elevation={3} sx={{ borderRadius: 4, overflow: 'hidden' }}>
                {/* Profile Header */}
                <Box sx={{ bgcolor: '#1A3263', py: 6, textAlign: 'center', color: 'white' }}>
                    <Avatar
                        sx={{
                            width: 100,
                            height: 100,
                            bgcolor: '#E8D1C5',
                            color: '#452829',
                            fontSize: '3rem',
                            mb: 2,
                            mx: 'auto',
                            border: '4px solid white'
                        }}
                    >
                        {user.email[0].toUpperCase()}
                    </Avatar>
                    <Typography variant="h3" sx={{ color: 'white' }}>User Profile</Typography>
                </Box>

                <Box sx={{ p: 4 }}>
                    <Grid container spacing={4}>
                        <Grid item xs={12} md={6}>
                            <Typography variant="h6" gutterBottom color="primary" sx={{ display: 'flex', alignItems: 'center' }}>
                                <EmailIcon sx={{ mr: 1, fontSize: 20 }} /> Account Information
                            </Typography>
                            <Box sx={{ mb: 3 }}>
                                <Typography variant="body2" color="text.secondary">Email Address</Typography>
                                <Typography variant="body1" sx={{ fontWeight: 600 }}>{user.email}</Typography>
                            </Box>
                            <Box>
                                <Typography variant="body2" color="text.secondary">Account Status</Typography>
                                <Chip label="active" color="success" size="small" sx={{ mt: 0.5 }} />
                            </Box>
                        </Grid>

                        <Grid item xs={12} md={6}>
                            <Typography variant="h6" gutterBottom color="primary" sx={{ display: 'flex', alignItems: 'center' }}>
                                <SecurityIcon sx={{ mr: 1, fontSize: 20 }} /> Permissions & Role
                            </Typography>
                            <Box sx={{ mb: 3 }}>
                                <Typography variant="body2" color="text.secondary">Current Role</Typography>
                                <Chip
                                    label={user.role || 'patient'}
                                    sx={{
                                        mt: 0.5,
                                        bgcolor: '#E8D1C5',
                                        color: '#452829',
                                        fontWeight: 700,
                                        textTransform: 'uppercase'
                                    }}
                                />
                            </Box>
                            <Box>
                                <Typography variant="body2" color="text.secondary">Identity Provider</Typography>
                                <Typography variant="body1" sx={{ fontWeight: 600 }}>Email/Password</Typography>
                            </Box>
                        </Grid>
                    </Grid>

                    <Divider sx={{ my: 4 }} />

                    <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
                        <Button variant="outlined" color="primary">Change Password</Button>
                        <Button variant="contained" sx={{ bgcolor: '#1A3263' }}>Edit Profile</Button>
                    </Box>
                </Box>
            </Paper>

            <Box sx={{ mt: 4, p: 3, bgcolor: 'rgba(26, 50, 99, 0.04)', borderRadius: 3 }}>
                <Typography variant="body2" color="text.secondary">
                    <strong>Note:</strong> Your profile information is used to personalize your analysis results. Advanced medical history tracking will be available in the next industry upgrade.
                </Typography>
            </Box>
        </Container>
    );
};

export default ProfilePage;
