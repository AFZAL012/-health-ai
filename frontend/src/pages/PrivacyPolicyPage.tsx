import { Box, Container, Typography, Divider } from '@mui/material';
import { motion } from 'framer-motion';
import ShieldIcon from '@mui/icons-material/Shield';

const PrivacyPolicyPage = () => (
    <Box sx={{ minHeight: '100vh', pt: { xs: 10, md: 14 }, pb: 10, bgcolor: '#F3E8DF' }}>
        <Container maxWidth="md">
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
                <Box sx={{ display: 'inline-flex', p: 1.5, borderRadius: '16px', bgcolor: '#2D1B1C', color: '#E8D1C5', mb: 4 }}>
                    <ShieldIcon />
                </Box>
                <Typography variant="h3" sx={{ fontWeight: 900, mb: 1, fontFamily: "'Outfit', sans-serif" }}>
                    Privacy Policy
                </Typography>
                <Typography variant="body2" sx={{ color: 'text.secondary', mb: 6 }}>
                    Last updated: March 4, 2026
                </Typography>

                <Box sx={{ bgcolor: 'white', borderRadius: '24px', p: { xs: 4, md: 6 }, boxShadow: '0 20px 60px rgba(69,40,41,0.05)' }}>
                    {[
                        {
                            title: '1. Information We Collect',
                            body: 'We collect information you provide directly to us, such as when you create an account (email address), or when you use our symptom analysis tools (selected symptoms). We do not collect personally identifying health information beyond what you voluntarily submit.'
                        },
                        {
                            title: '2. How We Use Your Information',
                            body: 'We use the information we collect to provide, maintain, and improve our services, to process transactions, to send you technical notices and support messages, and to respond to your comments and questions.'
                        },
                        {
                            title: '3. Data Security',
                            body: 'We use industry-standard AES-256 encryption to protect your data in transit and at rest. Your health analysis data is anonymized and processed in real-time. We never sell your personal data to third parties.'
                        },
                        {
                            title: '4. Data Retention',
                            body: 'We retain your account information and analysis history for as long as your account is active. You may request deletion of your account and associated data at any time by contacting our support team.'
                        },
                        {
                            title: '5. Cookies',
                            body: 'We use only essential session cookies required for authentication. We do not use tracking or advertising cookies.'
                        },
                        {
                            title: '6. Third-Party Services',
                            body: 'We use Gmail SMTP for transactional email delivery. No health data is shared with this service. We do not use any third-party analytics platforms that collect user behavior data.'
                        },
                        {
                            title: '7. Contact Us',
                            body: 'If you have any questions about this Privacy Policy, please contact us at privacy@healthai.dev.'
                        }
                    ].map((section, i) => (
                        <Box key={i} sx={{ mb: 4 }}>
                            <Typography variant="h6" sx={{ fontWeight: 900, mb: 1.5, color: '#2D1B1C' }}>{section.title}</Typography>
                            <Typography variant="body1" sx={{ color: 'text.secondary', lineHeight: 1.8 }}>{section.body}</Typography>
                            {i < 6 && <Divider sx={{ mt: 4 }} />}
                        </Box>
                    ))}
                </Box>
            </motion.div>
        </Container>
    </Box>
);

export default PrivacyPolicyPage;
