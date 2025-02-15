import pandas as pd
import numpy as np
from scipy import stats

class SleepDisorderDetector:
    """Real-time sleep disorder detection and analysis."""
    
    def __init__(self):
        self.disorder_patterns = {
            'insomnia': {
                'short_sleep': 6.0,  # hours
                'low_quality': 70,   # threshold
                'high_latency': 30   # minutes
            },
            'irregular_rhythm': {
                'time_variance': 2.0,  # hours
                'schedule_inconsistency': 1.5  # standard deviation threshold
            },
            'delayed_sleep': {
                'late_bedtime': 24,  # hour of day
                'late_wake': 9,      # hour of day
                'pattern_days': 5    # consecutive days
            }
        }

    def analyze_sleep_patterns(self, df):
        """Analyze sleep patterns for potential disorders."""
        results = {
            'detected_disorders': [],
            'risk_levels': {},
            'recommendations': []
        }

        # Check for insomnia patterns
        insomnia_risk = self._detect_insomnia(df)
        if insomnia_risk['risk_level'] > 0:
            results['detected_disorders'].append('Insomnia')
            results['risk_levels']['Insomnia'] = insomnia_risk

        # Check for irregular sleep rhythm
        rhythm_risk = self._detect_irregular_rhythm(df)
        if rhythm_risk['risk_level'] > 0:
            results['detected_disorders'].append('Irregular Sleep-Wake Rhythm')
            results['risk_levels']['Irregular Sleep-Wake Rhythm'] = rhythm_risk

        # Check for delayed sleep phase
        delayed_risk = self._detect_delayed_sleep(df)
        if delayed_risk['risk_level'] > 0:
            results['detected_disorders'].append('Delayed Sleep Phase')
            results['risk_levels']['Delayed Sleep Phase'] = delayed_risk

        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results['detected_disorders'])
        
        return results

    def _detect_insomnia(self, df):
        """Detect potential insomnia patterns."""
        short_sleep_days = len(df[df['duration'] < self.disorder_patterns['insomnia']['short_sleep']])
        low_quality_days = len(df[df['quality'] < self.disorder_patterns['insomnia']['low_quality']])
        
        risk_level = 0
        confidence = 0
        evidence = []
        
        if short_sleep_days >= len(df) * 0.3:  # 30% of nights
            risk_level += 0.4
            evidence.append(f"Short sleep duration detected in {short_sleep_days} nights")
            confidence += 0.3

        if low_quality_days >= len(df) * 0.3:
            risk_level += 0.3
            evidence.append(f"Poor sleep quality reported in {low_quality_days} nights")
            confidence += 0.3

        return {
            'risk_level': min(risk_level, 1.0),
            'confidence': confidence,
            'evidence': evidence
        }

    def _detect_irregular_rhythm(self, df):
        """Detect irregular sleep-wake rhythm."""
        sleep_time_std = df['sleep_start'].dt.hour.std()
        wake_time_std = df['sleep_end'].dt.hour.std()
        
        risk_level = 0
        confidence = 0
        evidence = []

        if sleep_time_std > self.disorder_patterns['irregular_rhythm']['schedule_inconsistency']:
            risk_level += 0.5
            evidence.append(f"Highly variable sleep times (std: {sleep_time_std:.2f} hours)")
            confidence += 0.4

        if wake_time_std > self.disorder_patterns['irregular_rhythm']['schedule_inconsistency']:
            risk_level += 0.3
            evidence.append(f"Inconsistent wake times (std: {wake_time_std:.2f} hours)")
            confidence += 0.3

        return {
            'risk_level': min(risk_level, 1.0),
            'confidence': confidence,
            'evidence': evidence
        }

    def _detect_delayed_sleep(self, df):
        """Detect delayed sleep phase pattern."""
        late_bedtimes = len(df[df['sleep_start'].dt.hour >= self.disorder_patterns['delayed_sleep']['late_bedtime']])
        late_wakes = len(df[df['sleep_end'].dt.hour >= self.disorder_patterns['delayed_sleep']['late_wake']])
        
        risk_level = 0
        confidence = 0
        evidence = []

        if late_bedtimes >= len(df) * 0.4:
            risk_level += 0.4
            evidence.append(f"Late bedtime pattern detected in {late_bedtimes} nights")
            confidence += 0.3

        if late_wakes >= len(df) * 0.4:
            risk_level += 0.4
            evidence.append(f"Late wake time pattern detected in {late_wakes} nights")
            confidence += 0.3

        return {
            'risk_level': min(risk_level, 1.0),
            'confidence': confidence,
            'evidence': evidence
        }

    def _generate_recommendations(self, detected_disorders):
        """Generate recommendations based on detected disorders."""
        recommendations = []
        
        if 'Insomnia' in detected_disorders:
            recommendations.extend([
                "Maintain a consistent sleep schedule",
                "Create a relaxing bedtime routine",
                "Avoid screens 1-2 hours before bed",
                "Consider consulting a sleep specialist"
            ])
            
        if 'Irregular Sleep-Wake Rhythm' in detected_disorders:
            recommendations.extend([
                "Set fixed wake-up and bedtime hours",
                "Expose yourself to natural light during the day",
                "Avoid long naps, especially in the late afternoon",
                "Create a structured daily routine"
            ])
            
        if 'Delayed Sleep Phase' in detected_disorders:
            recommendations.extend([
                "Gradually adjust bedtime earlier by 15 minutes each week",
                "Use bright light therapy in the morning",
                "Avoid bright lights in the evening",
                "Maintain a consistent wake time, even on weekends"
            ])
            
        return recommendations
