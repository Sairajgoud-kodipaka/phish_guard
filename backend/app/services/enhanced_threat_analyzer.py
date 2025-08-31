"""
Enhanced Threat Analyzer Service
Uses machine learning models trained on the spam dataset for email classification
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
import pickle
from pathlib import Path
import structlog
from typing import Optional, Dict, Any, Tuple
import re
import string

logger = structlog.get_logger()

class EnhancedThreatAnalyzer:
    """Enhanced threat analyzer using ML models trained on spam dataset"""
    
    def __init__(self, model_dir: str = "models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
        
        self.vectorizer = None
        self.classifier = None
        self.model_pipeline = None
        self.is_trained = False
        
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for analysis"""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    async def train_model(self, dataset_path: str) -> bool:
        """Train the ML model on the spam dataset"""
        try:
            logger.info("🤖 Training ML model on spam dataset...")
            
            # Load the dataset
            df = pd.read_csv(dataset_path)
            
            # Check if we have the expected columns
            if 'text' not in df.columns or 'label' not in df.columns:
                # Try to find similar columns
                text_col = None
                label_col = None
                
                for col in df.columns:
                    if 'text' in col.lower() or 'message' in col.lower() or 'content' in col.lower():
                        text_col = col
                    if 'label' in col.lower() or 'spam' in col.lower() or 'type' in col.lower():
                        label_col = col
                
                if text_col is None or label_col is None:
                    logger.error(f"❌ Could not find text and label columns. Available columns: {list(df.columns)}")
                    return False
                
                df = df.rename(columns={text_col: 'text', label_col: 'label'})
            
            # Preprocess the text data
            df['processed_text'] = df['text'].apply(self.preprocess_text)
            
            # Remove rows with empty text
            df = df[df['processed_text'].str.len() > 0]
            
            # Convert labels to binary (spam = 1, ham = 0)
            if df['label'].dtype == 'object':
                # Convert string labels to numeric
                df['label_binary'] = df['label'].map(lambda x: 1 if 'spam' in str(x).lower() else 0)
            else:
                df['label_binary'] = df['label']
            
            logger.info(f"📊 Dataset loaded: {len(df)} emails")
            logger.info(f"📈 Spam emails: {df['label_binary'].sum()}")
            logger.info(f"📉 Ham emails: {len(df) - df['label_binary'].sum()}")
            
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(
                df['processed_text'], 
                df['label_binary'], 
                test_size=0.2, 
                random_state=42
            )
            
            # Create and train the pipeline
            self.model_pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english')),
                ('classifier', MultinomialNB())
            ])
            
            # Train the model
            self.model_pipeline.fit(X_train, y_train)
            
            # Evaluate the model
            y_pred = self.model_pipeline.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            logger.info(f"✅ Model trained successfully!")
            logger.info(f"📊 Test accuracy: {accuracy:.4f}")
            
            # Save the model
            model_file = self.model_dir / "spam_classifier.pkl"
            with open(model_file, 'wb') as f:
                pickle.dump(self.model_pipeline, f)
            
            logger.info(f"💾 Model saved to {model_file}")
            
            self.is_trained = True
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to train model: {e}")
            return False
    
    async def load_model(self) -> bool:
        """Load a pre-trained model"""
        try:
            model_file = self.model_dir / "spam_classifier.pkl"
            
            if not model_file.exists():
                logger.warning("No pre-trained model found")
                return False
            
            with open(model_file, 'rb') as f:
                self.model_pipeline = pickle.load(f)
            
            self.is_trained = True
            logger.info("✅ Pre-trained model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            return False
    
    async def analyze_email(self, email_content: str) -> Dict[str, Any]:
        """Analyze an email for threats using the trained model"""
        try:
            if not self.is_trained:
                logger.warning("Model not trained. Loading pre-trained model...")
                if not await self.load_model():
                    return {
                        'threat_level': 'unknown',
                        'confidence': 0.0,
                        'is_spam': False,
                        'error': 'Model not available'
                    }
            
            # Preprocess the email content
            processed_content = self.preprocess_text(email_content)
            
            if not processed_content:
                return {
                    'threat_level': 'unknown',
                    'confidence': 0.0,
                    'is_spam': False,
                    'error': 'Empty or invalid content'
                }
            
            # Make prediction
            prediction = self.model_pipeline.predict([processed_content])[0]
            confidence = self.model_pipeline.predict_proba([processed_content])[0].max()
            
            # Determine threat level
            if prediction == 1:  # Spam
                if confidence > 0.8:
                    threat_level = 'high'
                elif confidence > 0.6:
                    threat_level = 'medium'
                else:
                    threat_level = 'low'
            else:  # Ham
                threat_level = 'safe'
            
            result = {
                'threat_level': threat_level,
                'confidence': float(confidence),
                'is_spam': bool(prediction),
                'processed_content': processed_content,
                'model_used': 'ML Spam Classifier'
            }
            
            logger.info(f"🔍 Email analyzed: {threat_level} threat level, confidence: {confidence:.3f}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze email: {e}")
            return {
                'threat_level': 'error',
                'confidence': 0.0,
                'is_spam': False,
                'error': str(e)
            }
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get information about the trained model"""
        return {
            'is_trained': self.is_trained,
            'model_directory': str(self.model_dir),
            'model_file_exists': (self.model_dir / "spam_classifier.pkl").exists(),
            'model_type': 'TF-IDF + Multinomial Naive Bayes'
        }

# Global enhanced threat analyzer instance
enhanced_analyzer = EnhancedThreatAnalyzer()
