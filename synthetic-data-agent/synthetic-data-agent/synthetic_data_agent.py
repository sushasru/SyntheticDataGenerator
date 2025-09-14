#!/usr/bin/env python3
import json
import random
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import uuid
from faker import Faker
import numpy as np
import os
import io
import re

class SyntheticDataAgent:
    def __init__(self):
        self.fake = Faker()
        
    def analyze_uploaded_file(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Analyze uploaded files to understand data patterns"""
        try:
            print(f"🤖 Agent: Analyzing uploaded {file_type} file...")
            
            if file_type.lower() == 'csv':
                return self._analyze_csv_file(file_path)
            elif file_type.lower() in ['xlsx', 'xls']:
                return self._analyze_excel_file(file_path)
            elif file_type.lower() == 'pdf':
                return self._analyze_pdf_file(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
                
        except Exception as e:
            print(f"❌ Error analyzing file: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_csv_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze CSV file patterns"""
        try:
            # Try different encodings
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    if len(df.columns) > 1:
                        break
                except:
                    continue
            
            return self._extract_data_patterns(df)
            
        except Exception as e:
            raise Exception(f"Error reading CSV: {str(e)}")
    
    def _analyze_excel_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze Excel file patterns"""
        try:
            df = pd.read_excel(file_path, sheet_name=0)
            return self._extract_data_patterns(df)
        except Exception as e:
            raise Exception(f"Error reading Excel file: {str(e)}")
    
    def _analyze_pdf_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze PDF file - simplified version"""
        try:
            # For demo purposes, return a simple pattern
            return {
                'file_type': 'pdf_text',
                'columns': ['id', 'name', 'value', 'date'],
                'num_rows': 100,
                'num_columns': 4,
                'patterns': {
                    'emails': ['user@company.com'],
                    'numbers': ['100', '200', '300']
                }
            }
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
    
    def _extract_data_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract statistical patterns from DataFrame"""
        patterns = {
            'columns': list(df.columns),
            'num_rows': len(df),
            'num_columns': len(df.columns),
            'column_types': {},
            'value_patterns': {},
            'sample_data': df.head(3).to_dict('records') if len(df) > 0 else []
        }
        
        for col in df.columns:
            col_data = df[col].dropna()
            if len(col_data) == 0:
                continue
                
            patterns['column_types'][col] = str(df[col].dtype)
            
            if df[col].dtype in ['object', 'string']:
                patterns['value_patterns'][col] = {
                    'type': 'categorical',
                    'unique_values': list(col_data.unique())[:10],
                    'most_common': col_data.value_counts().head(3).to_dict()
                }
            elif df[col].dtype in ['int64', 'float64']:
                patterns['value_patterns'][col] = {
                    'type': 'numeric',
                    'min': float(col_data.min()),
                    'max': float(col_data.max()),
                    'mean': float(col_data.mean())
                }
        
        return patterns
    
    def generate_from_file_patterns(self, patterns: Dict[str, Any], num_records: int) -> pd.DataFrame:
        """Generate synthetic data based on learned file patterns"""
        if 'error' in patterns:
            raise Exception(f"Cannot generate from patterns: {patterns['error']}")
        
        data = []
        columns = patterns.get('columns', ['id', 'name', 'value'])
        
        for _ in range(num_records):
            record = {}
            for col in columns:
                if col in patterns.get('value_patterns', {}):
                    col_pattern = patterns['value_patterns'][col]
                    if col_pattern['type'] == 'categorical':
                        unique_vals = col_pattern.get('unique_values', [])
                        if unique_vals:
                            record[col] = random.choice(unique_vals)
                        else:
                            record[col] = self.fake.word()
                    elif col_pattern['type'] == 'numeric':
                        min_val = col_pattern.get('min', 0)
                        max_val = col_pattern.get('max', 1000)
                        record[col] = round(random.uniform(min_val, max_val), 2)
                else:
                    # Fallback generation
                    if 'id' in col.lower():
                        record[col] = random.randint(1000, 9999)
                    elif 'name' in col.lower():
                        record[col] = self.fake.name()
                    elif 'email' in col.lower():
                        record[col] = self.fake.email()
                    elif 'date' in col.lower():
                        record[col] = self.fake.date()
                    else:
                        record[col] = self.fake.word()
            
            data.append(record)
        
        return pd.DataFrame(data)
    
    def generate_data(self, request: str, custom_schema: Dict[str, Dict] = None, file_patterns: Dict[str, Any] = None) -> pd.DataFrame:
        """Main method - generate synthetic data"""
        # Extract number of records from request
        import re
        numbers = re.findall(r'\d+', request)
        num_records = int(numbers[0]) if numbers else 100
        
        if file_patterns:
            return self.generate_from_file_patterns(file_patterns, num_records)
        
        # Simple default generation
        data = []
        for i in range(num_records):
            data.append({
                'id': i + 1,
                'name': self.fake.name(),
                'email': self.fake.email(),
                'value': round(random.uniform(10, 1000), 2),
                'date': self.fake.date()
            })
        
        return pd.DataFrame(data)

# Test the agent
if __name__ == "__main__":
    agent = SyntheticDataAgent()
    print("Synthetic Data Agent with File Upload Ready!")
