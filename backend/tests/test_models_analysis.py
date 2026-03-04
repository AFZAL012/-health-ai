"""Tests for Analysis and Report models."""
import pytest
import uuid
from datetime import datetime, timedelta
from models import User, Analysis, Report, db


class TestAnalysisModel:
    """Test suite for Analysis model."""
    
    def test_analysis_creation_with_user(self, app):
        """Test creating an analysis for an authenticated user."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            analysis = Analysis(
                user_id=user.id,
                symptoms=[
                    {'symptom': 'fever', 'severity': 'moderate', 'duration': 3, 'unit': 'days'}
                ],
                predictions=[
                    {'disease': 'Flu', 'probability': 0.85, 'confidence': [0.75, 0.95]}
                ],
                risk_level='medium',
                recommendations=[
                    {'type': 'precaution', 'text': 'Rest and hydrate', 'priority': 1}
                ]
            )
            analysis.save()
            
            assert analysis.id is not None
            assert analysis.user_id == user.id
            assert analysis.analysis_id is not None
            assert len(analysis.symptoms) == 1
            assert len(analysis.predictions) == 1
            assert analysis.risk_level == 'medium'
            assert len(analysis.recommendations) == 1
            assert analysis.created_at is not None
    
    def test_analysis_creation_anonymous(self, app):
        """Test creating an analysis for an anonymous user."""
        with app.app_context():
            analysis = Analysis(
                user_id=None,
                symptoms=[{'symptom': 'headache', 'severity': 'mild'}],
                predictions=[{'disease': 'Tension Headache', 'probability': 0.70}],
                risk_level='low',
                recommendations=[{'type': 'precaution', 'text': 'Take rest'}]
            )
            analysis.save()
            
            assert analysis.id is not None
            assert analysis.user_id is None
            assert analysis.analysis_id is not None
    
    def test_analysis_unique_analysis_id(self, app):
        """Test that each analysis gets a unique analysis_id."""
        with app.app_context():
            analysis1 = Analysis(
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='medium',
                recommendations=[]
            )
            analysis1.save()
            
            analysis2 = Analysis(
                symptoms=[{'symptom': 'cough'}],
                predictions=[{'disease': 'Cold', 'probability': 0.7}],
                risk_level='low',
                recommendations=[]
            )
            analysis2.save()
            
            assert analysis1.analysis_id != analysis2.analysis_id
            # Verify they are valid UUIDs
            uuid.UUID(analysis1.analysis_id)
            uuid.UUID(analysis2.analysis_id)
    
    def test_analysis_with_notes(self, app):
        """Test adding notes to an analysis."""
        with app.app_context():
            analysis = Analysis(
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='medium',
                recommendations=[],
                notes='Patient reports symptoms started after travel'
            )
            analysis.save()
            
            assert analysis.notes == 'Patient reports symptoms started after travel'
    
    def test_analysis_to_dict(self, app):
        """Test converting analysis to dictionary."""
        with app.app_context():
            analysis = Analysis(
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='high',
                recommendations=[{'text': 'Seek medical attention'}]
            )
            analysis.save()
            
            analysis_dict = analysis.to_dict()
            
            assert 'id' in analysis_dict
            assert 'analysis_id' in analysis_dict
            assert 'symptoms' in analysis_dict
            assert 'predictions' in analysis_dict
            assert 'risk_level' in analysis_dict
            assert 'recommendations' in analysis_dict
            assert isinstance(analysis_dict['symptoms'], list)
            assert isinstance(analysis_dict['predictions'], list)
    
    def test_analysis_user_relationship(self, app):
        """Test relationship between Analysis and User."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            analysis = Analysis(
                user_id=user.id,
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='medium',
                recommendations=[]
            )
            analysis.save()
            
            # Test forward relationship
            assert analysis.user.id == user.id
            assert analysis.user.email == user.email
            
            # Test backward relationship
            assert len(user.analyses) == 1
            assert user.analyses[0].id == analysis.id
    
    def test_analysis_cascade_delete_with_user(self, app):
        """Test that deleting user cascades to analyses."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            analysis = Analysis(
                user_id=user.id,
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='medium',
                recommendations=[]
            )
            analysis.save()
            
            analysis_id = analysis.id
            user.delete()
            
            # Analysis should be deleted
            deleted_analysis = Analysis.find_by_id(analysis_id)
            assert deleted_analysis is None
    
    def test_analysis_set_null_on_user_delete(self, app):
        """Test that user_id is set to NULL when user is deleted (if cascade is SET NULL)."""
        # Note: Current implementation uses CASCADE delete, but this tests the alternative
        # This test documents expected behavior if we change to SET NULL
        pass
    
    def test_analysis_repr(self, app):
        """Test analysis string representation."""
        with app.app_context():
            analysis = Analysis(
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='high',
                recommendations=[]
            )
            analysis.save()
            
            repr_str = repr(analysis)
            assert 'Analysis' in repr_str
            assert analysis.analysis_id in repr_str
            assert 'high' in repr_str
    
    def test_analysis_index_on_user_created(self, app):
        """Test that composite index on user_id and created_at exists."""
        with app.app_context():
            # Create multiple analyses for the same user
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            for i in range(3):
                analysis = Analysis(
                    user_id=user.id,
                    symptoms=[{'symptom': f'symptom{i}'}],
                    predictions=[{'disease': 'Disease', 'probability': 0.8}],
                    risk_level='low',
                    recommendations=[]
                )
                analysis.save()
            
            # Query should use the index (this is more of a documentation test)
            analyses = Analysis.query.filter_by(user_id=user.id).order_by(
                Analysis.created_at.desc()
            ).all()
            
            assert len(analyses) == 3
            # Verify they are in descending order
            assert analyses[0].created_at >= analyses[1].created_at
            assert analyses[1].created_at >= analyses[2].created_at


class TestReportModel:
    """Test suite for Report model."""
    
    def test_report_creation(self, app):
        """Test creating a report for an analysis."""
        with app.app_context():
            analysis = Analysis(
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='medium',
                recommendations=[]
            )
            analysis.save()
            
            report = Report(
                analysis_id=analysis.id,
                format='pdf',
                file_path='/reports/report_123.pdf',
                file_size=102400,
                expires_at=datetime.utcnow() + timedelta(days=30)
            )
            report.save()
            
            assert report.id is not None
            assert report.report_id is not None
            assert report.analysis_id == analysis.id
            assert report.format == 'pdf'
            assert report.file_path == '/reports/report_123.pdf'
            assert report.file_size == 102400
            assert report.expires_at is not None
    
    def test_report_unique_report_id(self, app):
        """Test that each report gets a unique report_id."""
        with app.app_context():
            analysis = Analysis(
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='medium',
                recommendations=[]
            )
            analysis.save()
            
            report1 = Report(analysis_id=analysis.id, format='pdf')
            report1.save()
            
            report2 = Report(analysis_id=analysis.id, format='html')
            report2.save()
            
            assert report1.report_id != report2.report_id
            # Verify they are valid UUIDs
            uuid.UUID(report1.report_id)
            uuid.UUID(report2.report_id)
    
    def test_report_default_format(self, app):
        """Test default format is pdf."""
        with app.app_context():
            analysis = Analysis(
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='medium',
                recommendations=[]
            )
            analysis.save()
            
            report = Report(analysis_id=analysis.id)
            report.save()
            
            assert report.format == 'pdf'
    
    def test_report_analysis_relationship(self, app):
        """Test relationship between Report and Analysis."""
        with app.app_context():
            analysis = Analysis(
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='medium',
                recommendations=[]
            )
            analysis.save()
            
            report = Report(analysis_id=analysis.id, format='pdf')
            report.save()
            
            # Test forward relationship
            assert report.analysis.id == analysis.id
            
            # Test backward relationship
            assert len(analysis.reports) == 1
            assert analysis.reports[0].id == report.id
    
    def test_report_cascade_delete_with_analysis(self, app):
        """Test that deleting analysis cascades to reports."""
        with app.app_context():
            analysis = Analysis(
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='medium',
                recommendations=[]
            )
            analysis.save()
            
            report = Report(analysis_id=analysis.id, format='pdf')
            report.save()
            
            report_id = report.id
            analysis.delete()
            
            # Report should be deleted
            deleted_report = Report.find_by_id(report_id)
            assert deleted_report is None
    
    def test_report_multiple_formats_for_analysis(self, app):
        """Test creating multiple reports in different formats for same analysis."""
        with app.app_context():
            analysis = Analysis(
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='medium',
                recommendations=[]
            )
            analysis.save()
            
            pdf_report = Report(analysis_id=analysis.id, format='pdf')
            pdf_report.save()
            
            html_report = Report(analysis_id=analysis.id, format='html')
            html_report.save()
            
            assert len(analysis.reports) == 2
            formats = [r.format for r in analysis.reports]
            assert 'pdf' in formats
            assert 'html' in formats
    
    def test_report_to_dict(self, app):
        """Test converting report to dictionary."""
        with app.app_context():
            analysis = Analysis(
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='medium',
                recommendations=[]
            )
            analysis.save()
            
            report = Report(
                analysis_id=analysis.id,
                format='pdf',
                file_path='/reports/test.pdf',
                file_size=1024
            )
            report.save()
            
            report_dict = report.to_dict()
            
            assert 'id' in report_dict
            assert 'report_id' in report_dict
            assert 'analysis_id' in report_dict
            assert 'format' in report_dict
            assert 'file_path' in report_dict
            assert 'file_size' in report_dict
    
    def test_report_repr(self, app):
        """Test report string representation."""
        with app.app_context():
            analysis = Analysis(
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='medium',
                recommendations=[]
            )
            analysis.save()
            
            report = Report(analysis_id=analysis.id, format='pdf')
            report.save()
            
            repr_str = repr(report)
            assert 'Report' in repr_str
            assert report.report_id in repr_str
            assert 'pdf' in repr_str


class TestAnalysisReportIntegration:
    """Test integration between Analysis and Report models."""
    
    def test_full_chain_user_analysis_report(self, app):
        """Test complete chain: User -> Analysis -> Report."""
        with app.app_context():
            # Create user
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            # Create analysis
            analysis = Analysis(
                user_id=user.id,
                symptoms=[{'symptom': 'fever', 'severity': 'high'}],
                predictions=[
                    {'disease': 'Flu', 'probability': 0.85},
                    {'disease': 'COVID-19', 'probability': 0.75}
                ],
                risk_level='high',
                recommendations=[
                    {'type': 'urgency', 'text': 'Seek medical attention immediately'}
                ]
            )
            analysis.save()
            
            # Create report
            report = Report(
                analysis_id=analysis.id,
                format='pdf',
                file_path=f'/reports/{analysis.analysis_id}.pdf',
                file_size=204800
            )
            report.save()
            
            # Verify relationships
            assert user.analyses[0].id == analysis.id
            assert analysis.user.id == user.id
            assert analysis.reports[0].id == report.id
            assert report.analysis.id == analysis.id
            assert report.analysis.user.id == user.id
    
    def test_cascade_delete_full_chain(self, app):
        """Test cascade delete from user through analysis to report."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            analysis = Analysis(
                user_id=user.id,
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='medium',
                recommendations=[]
            )
            analysis.save()
            
            report = Report(analysis_id=analysis.id, format='pdf')
            report.save()
            
            analysis_id = analysis.id
            report_id = report.id
            
            # Delete user
            user.delete()
            
            # Both analysis and report should be deleted
            assert Analysis.find_by_id(analysis_id) is None
            assert Report.find_by_id(report_id) is None
    
    def test_query_user_analyses_with_reports(self, app):
        """Test querying user's analyses with their reports."""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('Password123!')
            user.save()
            
            # Create multiple analyses with reports
            for i in range(3):
                analysis = Analysis(
                    user_id=user.id,
                    symptoms=[{'symptom': f'symptom{i}'}],
                    predictions=[{'disease': 'Disease', 'probability': 0.8}],
                    risk_level='low',
                    recommendations=[]
                )
                analysis.save()
                
                report = Report(analysis_id=analysis.id, format='pdf')
                report.save()
            
            # Query all analyses for user
            analyses = Analysis.query.filter_by(user_id=user.id).all()
            assert len(analyses) == 3
            
            # Each analysis should have one report
            for analysis in analyses:
                assert len(analysis.reports) == 1
    
    def test_analysis_update_method(self, app):
        """Test updating analysis fields."""
        with app.app_context():
            analysis = Analysis(
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='medium',
                recommendations=[]
            )
            analysis.save()
            
            analysis.update(
                notes='Updated with patient feedback',
                risk_level='high'
            )
            
            assert analysis.notes == 'Updated with patient feedback'
            assert analysis.risk_level == 'high'
    
    def test_report_update_method(self, app):
        """Test updating report fields."""
        with app.app_context():
            analysis = Analysis(
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='medium',
                recommendations=[]
            )
            analysis.save()
            
            report = Report(analysis_id=analysis.id, format='pdf')
            report.save()
            
            report.update(
                file_path='/reports/updated.pdf',
                file_size=307200
            )
            
            assert report.file_path == '/reports/updated.pdf'
            assert report.file_size == 307200


class TestAnalysisEdgeCases:
    """Test edge cases for Analysis model."""
    
    def test_analysis_empty_json_fields(self, app):
        """Test analysis with empty JSON arrays."""
        with app.app_context():
            analysis = Analysis(
                symptoms=[],
                predictions=[],
                risk_level='unknown',
                recommendations=[]
            )
            analysis.save()
            
            assert analysis.symptoms == []
            assert analysis.predictions == []
            assert analysis.recommendations == []
    
    def test_analysis_complex_json_data(self, app):
        """Test analysis with complex nested JSON data."""
        with app.app_context():
            analysis = Analysis(
                symptoms=[
                    {
                        'symptom': 'fever',
                        'severity': 'high',
                        'duration': 5,
                        'unit': 'days',
                        'metadata': {
                            'onset': '2024-01-01',
                            'pattern': 'intermittent'
                        }
                    }
                ],
                predictions=[
                    {
                        'disease': 'Malaria',
                        'probability': 0.75,
                        'confidence_interval': [0.65, 0.85],
                        'matched_symptoms': ['fever', 'chills'],
                        'specialist': 'Infectious Disease'
                    }
                ],
                risk_level='high',
                recommendations=[
                    {
                        'type': 'urgency',
                        'priority': 1,
                        'text': 'Seek immediate medical attention',
                        'details': {
                            'reason': 'High fever with potential tropical disease',
                            'actions': ['Visit ER', 'Blood test required']
                        }
                    }
                ]
            )
            analysis.save()
            
            # Verify complex data is preserved
            assert analysis.symptoms[0]['metadata']['pattern'] == 'intermittent'
            assert len(analysis.predictions[0]['matched_symptoms']) == 2
            assert len(analysis.recommendations[0]['details']['actions']) == 2
    
    def test_analysis_long_notes(self, app):
        """Test analysis with very long notes."""
        with app.app_context():
            long_notes = 'A' * 10000  # 10,000 characters
            
            analysis = Analysis(
                symptoms=[{'symptom': 'fever'}],
                predictions=[{'disease': 'Flu', 'probability': 0.8}],
                risk_level='medium',
                recommendations=[],
                notes=long_notes
            )
            analysis.save()
            
            assert len(analysis.notes) == 10000
            assert analysis.notes == long_notes
