"""Tests for Disease, Symptom, and DiseaseTranslation models."""
import pytest
from models import Disease, Symptom, DiseaseTranslation, db


class TestDiseaseModel:
    """Test suite for Disease model."""
    
    def test_disease_creation(self, app):
        """Test creating a disease with valid data."""
        with app.app_context():
            disease = Disease(
                name='Influenza',
                description='A viral infection that attacks the respiratory system',
                severity='moderate',
                common_symptoms=['fever', 'cough', 'fatigue'],
                specialist='General Practitioner',
                precautions=['Rest', 'Hydration', 'Antiviral medication'],
                lifestyle_recommendations=['Avoid crowded places', 'Wash hands frequently'],
                urgency_guidelines='Seek immediate care if breathing difficulty occurs'
            )
            disease.save()
            
            assert disease.id is not None
            assert disease.name == 'Influenza'
            assert disease.description == 'A viral infection that attacks the respiratory system'
            assert disease.severity == 'moderate'
            assert disease.common_symptoms == ['fever', 'cough', 'fatigue']
            assert disease.specialist == 'General Practitioner'
            assert disease.precautions == ['Rest', 'Hydration', 'Antiviral medication']
            assert disease.lifestyle_recommendations == ['Avoid crowded places', 'Wash hands frequently']
            assert disease.urgency_guidelines == 'Seek immediate care if breathing difficulty occurs'
            assert disease.created_at is not None
            assert disease.updated_at is not None
    
    def test_disease_unique_name_constraint(self, app):
        """Test that duplicate disease names are rejected."""
        with app.app_context():
            disease1 = Disease(name='Diabetes')
            disease1.save()
            
            disease2 = Disease(name='Diabetes')
            
            with pytest.raises(Exception):  # SQLAlchemy IntegrityError
                disease2.save()
    
    def test_disease_minimal_fields(self, app):
        """Test creating disease with only required fields."""
        with app.app_context():
            disease = Disease(name='Common Cold')
            disease.save()
            
            assert disease.id is not None
            assert disease.name == 'Common Cold'
            assert disease.description is None
            assert disease.severity is None
    
    def test_disease_json_fields(self, app):
        """Test that JSON fields are properly stored and retrieved."""
        with app.app_context():
            symptoms = ['headache', 'nausea', 'dizziness']
            precautions = ['Rest', 'Medication', 'Avoid triggers']
            recommendations = ['Exercise', 'Healthy diet']
            
            disease = Disease(
                name='Migraine',
                common_symptoms=symptoms,
                precautions=precautions,
                lifestyle_recommendations=recommendations
            )
            disease.save()
            
            # Retrieve and verify
            retrieved = Disease.find_by_id(disease.id)
            assert retrieved.common_symptoms == symptoms
            assert retrieved.precautions == precautions
            assert retrieved.lifestyle_recommendations == recommendations
    
    def test_disease_to_dict(self, app):
        """Test disease to_dict conversion."""
        with app.app_context():
            disease = Disease(
                name='Asthma',
                severity='moderate',
                common_symptoms=['wheezing', 'shortness of breath']
            )
            disease.save()
            
            disease_dict = disease.to_dict()
            
            assert disease_dict['name'] == 'Asthma'
            assert disease_dict['severity'] == 'moderate'
            assert disease_dict['common_symptoms'] == ['wheezing', 'shortness of breath']
            assert 'created_at' in disease_dict
    
    def test_disease_repr(self, app):
        """Test disease string representation."""
        with app.app_context():
            disease = Disease(name='Pneumonia')
            disease.save()
            
            repr_str = repr(disease)
            assert 'Disease' in repr_str
            assert str(disease.id) in repr_str
            assert 'Pneumonia' in repr_str
    
    def test_disease_update(self, app):
        """Test updating disease fields."""
        with app.app_context():
            disease = Disease(name='Bronchitis', severity='mild')
            disease.save()
            
            disease.update(severity='moderate', specialist='Pulmonologist')
            
            assert disease.severity == 'moderate'
            assert disease.specialist == 'Pulmonologist'
    
    def test_disease_delete(self, app):
        """Test deleting a disease."""
        with app.app_context():
            disease = Disease(name='Test Disease')
            disease.save()
            disease_id = disease.id
            
            disease.delete()
            
            deleted = Disease.find_by_id(disease_id)
            assert deleted is None


class TestSymptomModel:
    """Test suite for Symptom model."""
    
    def test_symptom_creation(self, app):
        """Test creating a symptom with valid data."""
        with app.app_context():
            symptom = Symptom(
                canonical_name='Headache',
                category='Neurological',
                synonyms=['head pain', 'cephalalgia', 'cranial pain'],
                related_symptoms=['dizziness', 'nausea', 'sensitivity to light']
            )
            symptom.save()
            
            assert symptom.id is not None
            assert symptom.canonical_name == 'Headache'
            assert symptom.category == 'Neurological'
            assert symptom.synonyms == ['head pain', 'cephalalgia', 'cranial pain']
            assert symptom.related_symptoms == ['dizziness', 'nausea', 'sensitivity to light']
            assert symptom.created_at is not None
    
    def test_symptom_unique_canonical_name(self, app):
        """Test that duplicate canonical names are rejected."""
        with app.app_context():
            symptom1 = Symptom(canonical_name='Fever')
            symptom1.save()
            
            symptom2 = Symptom(canonical_name='Fever')
            
            with pytest.raises(Exception):  # SQLAlchemy IntegrityError
                symptom2.save()
    
    def test_symptom_minimal_fields(self, app):
        """Test creating symptom with only required fields."""
        with app.app_context():
            symptom = Symptom(canonical_name='Cough')
            symptom.save()
            
            assert symptom.id is not None
            assert symptom.canonical_name == 'Cough'
            assert symptom.category is None
            assert symptom.synonyms is None
    
    def test_symptom_json_fields(self, app):
        """Test that JSON fields are properly stored and retrieved."""
        with app.app_context():
            synonyms = ['pyrexia', 'high temperature', 'elevated temperature']
            related = ['chills', 'sweating', 'fatigue']
            
            symptom = Symptom(
                canonical_name='Fever',
                synonyms=synonyms,
                related_symptoms=related
            )
            symptom.save()
            
            # Retrieve and verify
            retrieved = Symptom.find_by_id(symptom.id)
            assert retrieved.synonyms == synonyms
            assert retrieved.related_symptoms == related
    
    def test_symptom_to_dict(self, app):
        """Test symptom to_dict conversion."""
        with app.app_context():
            symptom = Symptom(
                canonical_name='Nausea',
                category='Gastrointestinal',
                synonyms=['queasiness', 'upset stomach']
            )
            symptom.save()
            
            symptom_dict = symptom.to_dict()
            
            assert symptom_dict['canonical_name'] == 'Nausea'
            assert symptom_dict['category'] == 'Gastrointestinal'
            assert symptom_dict['synonyms'] == ['queasiness', 'upset stomach']
    
    def test_symptom_repr(self, app):
        """Test symptom string representation."""
        with app.app_context():
            symptom = Symptom(canonical_name='Fatigue')
            symptom.save()
            
            repr_str = repr(symptom)
            assert 'Symptom' in repr_str
            assert str(symptom.id) in repr_str
            assert 'Fatigue' in repr_str
    
    def test_symptom_update(self, app):
        """Test updating symptom fields."""
        with app.app_context():
            symptom = Symptom(canonical_name='Dizziness', category='General')
            symptom.save()
            
            symptom.update(category='Neurological', synonyms=['vertigo', 'lightheadedness'])
            
            assert symptom.category == 'Neurological'
            assert symptom.synonyms == ['vertigo', 'lightheadedness']
    
    def test_symptom_delete(self, app):
        """Test deleting a symptom."""
        with app.app_context():
            symptom = Symptom(canonical_name='Test Symptom')
            symptom.save()
            symptom_id = symptom.id
            
            symptom.delete()
            
            deleted = Symptom.find_by_id(symptom_id)
            assert deleted is None


class TestDiseaseTranslationModel:
    """Test suite for DiseaseTranslation model."""
    
    def test_translation_creation(self, app):
        """Test creating a disease translation with valid data."""
        with app.app_context():
            disease = Disease(name='Influenza')
            disease.save()
            
            translation = DiseaseTranslation(
                disease_id=disease.id,
                language_code='es',
                name='Gripe',
                description='Una infección viral que ataca el sistema respiratorio',
                precautions=['Descanso', 'Hidratación', 'Medicación antiviral']
            )
            translation.save()
            
            assert translation.id is not None
            assert translation.disease_id == disease.id
            assert translation.language_code == 'es'
            assert translation.name == 'Gripe'
            assert translation.description == 'Una infección viral que ataca el sistema respiratorio'
            assert translation.precautions == ['Descanso', 'Hidratación', 'Medicación antiviral']
            assert translation.created_at is not None
    
    def test_translation_unique_disease_language(self, app):
        """Test that duplicate disease-language combinations are rejected."""
        with app.app_context():
            disease = Disease(name='Diabetes')
            disease.save()
            
            translation1 = DiseaseTranslation(
                disease_id=disease.id,
                language_code='fr',
                name='Diabète'
            )
            translation1.save()
            
            translation2 = DiseaseTranslation(
                disease_id=disease.id,
                language_code='fr',
                name='Diabète Type 2'
            )
            
            with pytest.raises(Exception):  # Unique constraint violation
                translation2.save()
    
    def test_translation_multiple_languages(self, app):
        """Test that one disease can have multiple translations."""
        with app.app_context():
            disease = Disease(name='Asthma')
            disease.save()
            
            translation_es = DiseaseTranslation(
                disease_id=disease.id,
                language_code='es',
                name='Asma'
            )
            translation_es.save()
            
            translation_fr = DiseaseTranslation(
                disease_id=disease.id,
                language_code='fr',
                name='Asthme'
            )
            translation_fr.save()
            
            # Both should exist
            assert translation_es.id is not None
            assert translation_fr.id is not None
            assert translation_es.language_code == 'es'
            assert translation_fr.language_code == 'fr'
    
    def test_translation_relationship(self, app):
        """Test relationship between Disease and DiseaseTranslation."""
        with app.app_context():
            disease = Disease(name='Pneumonia')
            disease.save()
            
            translation = DiseaseTranslation(
                disease_id=disease.id,
                language_code='de',
                name='Lungenentzündung'
            )
            translation.save()
            
            # Test forward relationship
            assert translation.disease.id == disease.id
            assert translation.disease.name == 'Pneumonia'
            
            # Test backward relationship
            assert len(disease.translations) == 1
            assert disease.translations[0].language_code == 'de'
            assert disease.translations[0].name == 'Lungenentzündung'
    
    def test_translation_cascade_delete(self, app):
        """Test that deleting disease cascades to translations."""
        with app.app_context():
            disease = Disease(name='Bronchitis')
            disease.save()
            
            translation = DiseaseTranslation(
                disease_id=disease.id,
                language_code='it',
                name='Bronchite'
            )
            translation.save()
            
            translation_id = translation.id
            disease.delete()
            
            # Translation should be deleted
            deleted_translation = DiseaseTranslation.find_by_id(translation_id)
            assert deleted_translation is None
    
    def test_translation_minimal_fields(self, app):
        """Test creating translation with only required fields."""
        with app.app_context():
            disease = Disease(name='Migraine')
            disease.save()
            
            translation = DiseaseTranslation(
                disease_id=disease.id,
                language_code='pt',
                name='Enxaqueca'
            )
            translation.save()
            
            assert translation.id is not None
            assert translation.description is None
            assert translation.precautions is None
    
    def test_translation_json_precautions(self, app):
        """Test that JSON precautions field is properly stored."""
        with app.app_context():
            disease = Disease(name='Hypertension')
            disease.save()
            
            precautions = ['Reducir sal', 'Ejercicio regular', 'Medicación']
            
            translation = DiseaseTranslation(
                disease_id=disease.id,
                language_code='es',
                name='Hipertensión',
                precautions=precautions
            )
            translation.save()
            
            # Retrieve and verify
            retrieved = DiseaseTranslation.find_by_id(translation.id)
            assert retrieved.precautions == precautions
    
    def test_translation_to_dict(self, app):
        """Test translation to_dict conversion."""
        with app.app_context():
            disease = Disease(name='Arthritis')
            disease.save()
            
            translation = DiseaseTranslation(
                disease_id=disease.id,
                language_code='ja',
                name='関節炎',
                description='関節の炎症'
            )
            translation.save()
            
            translation_dict = translation.to_dict()
            
            assert translation_dict['disease_id'] == disease.id
            assert translation_dict['language_code'] == 'ja'
            assert translation_dict['name'] == '関節炎'
            assert translation_dict['description'] == '関節の炎症'
    
    def test_translation_repr(self, app):
        """Test translation string representation."""
        with app.app_context():
            disease = Disease(name='Allergy')
            disease.save()
            
            translation = DiseaseTranslation(
                disease_id=disease.id,
                language_code='zh',
                name='过敏'
            )
            translation.save()
            
            repr_str = repr(translation)
            assert 'DiseaseTranslation' in repr_str
            assert str(translation.id) in repr_str
            assert str(disease.id) in repr_str
            assert 'zh' in repr_str
    
    def test_translation_update(self, app):
        """Test updating translation fields."""
        with app.app_context():
            disease = Disease(name='Anemia')
            disease.save()
            
            translation = DiseaseTranslation(
                disease_id=disease.id,
                language_code='ru',
                name='Анемия'
            )
            translation.save()
            
            translation.update(
                description='Недостаток красных кровяных телец',
                precautions=['Железо', 'Витамины']
            )
            
            assert translation.description == 'Недостаток красных кровяных телец'
            assert translation.precautions == ['Железо', 'Витамины']


class TestDiseaseModelEdgeCases:
    """Test edge cases for Disease, Symptom, and DiseaseTranslation models."""
    
    def test_disease_empty_json_arrays(self, app):
        """Test disease with empty JSON arrays."""
        with app.app_context():
            disease = Disease(
                name='Test Disease',
                common_symptoms=[],
                precautions=[],
                lifestyle_recommendations=[]
            )
            disease.save()
            
            assert disease.common_symptoms == []
            assert disease.precautions == []
            assert disease.lifestyle_recommendations == []
    
    def test_symptom_empty_json_arrays(self, app):
        """Test symptom with empty JSON arrays."""
        with app.app_context():
            symptom = Symptom(
                canonical_name='Test Symptom',
                synonyms=[],
                related_symptoms=[]
            )
            symptom.save()
            
            assert symptom.synonyms == []
            assert symptom.related_symptoms == []
    
    def test_disease_long_text_fields(self, app):
        """Test disease with long text content."""
        with app.app_context():
            long_description = 'A' * 5000
            long_guidelines = 'B' * 5000
            
            disease = Disease(
                name='Long Text Disease',
                description=long_description,
                urgency_guidelines=long_guidelines
            )
            disease.save()
            
            retrieved = Disease.find_by_id(disease.id)
            assert len(retrieved.description) == 5000
            assert len(retrieved.urgency_guidelines) == 5000
    
    def test_translation_special_characters(self, app):
        """Test translation with special characters and unicode."""
        with app.app_context():
            disease = Disease(name='Test Disease')
            disease.save()
            
            translation = DiseaseTranslation(
                disease_id=disease.id,
                language_code='ar',
                name='مرض الاختبار',
                description='وصف المرض بالعربية'
            )
            translation.save()
            
            retrieved = DiseaseTranslation.find_by_id(translation.id)
            assert retrieved.name == 'مرض الاختبار'
            assert retrieved.description == 'وصف المرض بالعربية'
    
    def test_disease_find_all(self, app):
        """Test finding all diseases."""
        with app.app_context():
            disease1 = Disease(name='Disease 1')
            disease1.save()
            
            disease2 = Disease(name='Disease 2')
            disease2.save()
            
            all_diseases = Disease.find_all()
            assert len(all_diseases) >= 2
            disease_names = [d.name for d in all_diseases]
            assert 'Disease 1' in disease_names
            assert 'Disease 2' in disease_names
    
    def test_symptom_find_all(self, app):
        """Test finding all symptoms."""
        with app.app_context():
            symptom1 = Symptom(canonical_name='Symptom 1')
            symptom1.save()
            
            symptom2 = Symptom(canonical_name='Symptom 2')
            symptom2.save()
            
            all_symptoms = Symptom.find_all()
            assert len(all_symptoms) >= 2
            symptom_names = [s.canonical_name for s in all_symptoms]
            assert 'Symptom 1' in symptom_names
            assert 'Symptom 2' in symptom_names
