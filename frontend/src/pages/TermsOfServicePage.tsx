import { Box, Container, Typography, Divider } from '@mui/material';
import { motion } from 'framer-motion';
import GavelIcon from '@mui/icons-material/Gavel';

const TermsOfServicePage = () => (
    <Box sx={{ minHeight: '100vh', pt: { xs: 10, md: 14 }, pb: 10, bgcolor: '#F3E8DF' }}>
        <Container maxWidth="md">
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
                <Box sx={{ display: 'inline-flex', p: 1.5, borderRadius: '16px', bgcolor: '#2D1B1C', color: '#E8D1C5', mb: 4 }}>
                    <GavelIcon />
                </Box>
                <Typography variant="h3" sx={{ fontWeight: 900, mb: 1, fontFamily: "'Outfit', sans-serif" }}>
                    Terms of Service
                </Typography>
                <Typography variant="body2" sx={{ color: 'text.secondary', mb: 6 }}>
                    Last updated: March 4, 2026
                </Typography>

                <Box sx={{ bgcolor: 'white', borderRadius: '24px', p: { xs: 4, md: 6 }, boxShadow: '0 20px 60px rgba(69,40,41,0.05)' }}>
                    {[
                        {
                            title: '1. Acceptance of Terms',
                            body: 'By accessing or using Health AI, you agree to be bound by these Terms of Service. If you disagree with any part of these terms, you may not access the service.'
                        },
                        {
                            title: '2. Medical Disclaimer',
                            body: 'IMPORTANT: Health AI provides AI-generated symptom analysis for informational and educational purposes only. The results are NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or qualified health provider with any questions you may have regarding a medical condition.'
                        },
                        {
                            title: '3. Account Responsibilities',
                            body: 'You are responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account. You must notify us immediately of any unauthorized use of your account.'
                        },
                        {
                            title: '4. Acceptable Use',
                            body: 'You agree not to use Health AI to: (a) violate any applicable laws or regulations; (b) transmit harmful, offensive, or misleading content; (c) attempt to reverse-engineer the AI model or underlying systems; or (d) use the platform for any commercial purpose without explicit written consent.'
                        },
                        {
                            title: '5. Intellectual Property',
                            body: 'The Health AI platform, including its AI model, design, and codebase, is proprietary. All rights, titles, and interests remain with Health AI. You are granted a limited, non-exclusive, non-transferable license to use the service.'
                        },
                        {
                            title: '6. Limitation of Liability',
                            body: 'Health AI shall not be liable for any indirect, incidental, special, consequential, or punitive damages resulting from your use of, or inability to use, the service. This includes any damages arising from reliance on AI-generated health analysis results.'
                        },
                        {
                            title: '7. Changes to Terms',
                            body: 'We reserve the right to modify these terms at any time. We will notify users of significant changes via email or a prominent notice on the platform. Continued use of the service constitutes acceptance of the revised terms.'
                        },
                        {
                            title: '8. Contact',
                            body: 'For questions regarding these Terms of Service, please contact us at legal@healthai.dev.'
                        }
                    ].map((section, i) => (
                        <Box key={i} sx={{ mb: 4 }}>
                            <Typography variant="h6" sx={{ fontWeight: 900, mb: 1.5, color: '#2D1B1C' }}>{section.title}</Typography>
                            <Typography variant="body1" sx={{ color: 'text.secondary', lineHeight: 1.8 }}>{section.body}</Typography>
                            {i < 7 && <Divider sx={{ mt: 4 }} />}
                        </Box>
                    ))}
                </Box>
            </motion.div>
        </Container>
    </Box>
);

export default TermsOfServicePage;
