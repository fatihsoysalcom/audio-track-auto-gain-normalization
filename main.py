import math

def calculate_rms_loudness(samples):
    """Calculates RMS (Root Mean Square) loudness for a list of samples.
    RMS is a common metric related to perceived audio loudness.
    """
    if not samples:
        return 0.0
    # RMS = sqrt(sum(x^2) / N)
    sum_of_squares = sum(x**2 for x in samples)
    rms = math.sqrt(sum_of_squares / len(samples))
    return rms

def apply_auto_gain(samples, target_rms_loudness):
    """
    Applies a simple auto-gain adjustment to bring the track's RMS loudness
    closer to the target. This simulates the core function of 'Auto Gain'.
    """
    current_rms = calculate_rms_loudness(samples)
    if current_rms == 0: # Avoid division by zero if track is silent
        return samples # Cannot adjust if no sound
    
    # Calculate the gain factor needed to reach the target RMS
    gain_factor = target_rms_loudness / current_rms
    
    # Apply the gain to each sample and clamp values to a typical digital audio range (-1.0 to 1.0)
    # Clamping prevents 'clipping' (distortion) if the gain makes samples exceed the maximum level.
    adjusted_samples = [min(max(s * gain_factor, -1.0), 1.0) for s in samples]
    return adjusted_samples

# --- Main simulation --- 
if __name__ == "__main__":
    print("rekordbox Auto Gain Simulation (Conceptual)\n")

    # Simulate different audio tracks with varying initial loudness levels.
    # Samples are represented as float values between -1.0 and 1.0, like normalized digital audio.
    track1_samples = [0.5, 0.6, 0.4, 0.7, 0.55, 0.65, 0.45, 0.75] # Relatively loud
    track2_samples = [0.2, 0.3, 0.1, 0.25, 0.15, 0.35, 0.22, 0.18] # Quieter
    track3_samples = [0.8, 0.7, 0.9, 0.85, 0.75, 0.95, 0.82, 0.78] # Very loud, close to clipping
    track4_samples = [0.1, 0.05, 0.15, 0.08, 0.12, 0.07, 0.13, 0.09] # Very quiet

    all_tracks = {
        "Track A (Loud)": track1_samples,
        "Track B (Quiet)": track2_samples,
        "Track C (Very Loud)": track3_samples,
        "Track D (Very Quiet)": track4_samples,
    }

    target_loudness_rms = 0.4 # Our desired consistent RMS loudness for all tracks

    print(f"Target RMS Loudness: {target_loudness_rms:.2f}\n")

    processed_tracks = {}

    for name, samples in all_tracks.items():
        initial_rms = calculate_rms_loudness(samples)
        print(f"--- {name} ---")
        print(f"  Initial RMS Loudness: {initial_rms:.3f}")

        # Apply Auto Gain to adjust the track's volume
        adjusted_samples = apply_auto_gain(samples, target_loudness_rms)
        final_rms = calculate_rms_loudness(adjusted_samples)
        
        print(f"  Adjusted RMS Loudness: {final_rms:.3f}")
        # Check if any sample values hit the maximum limit after adjustment (potential clipping)
        if any(abs(s) >= 1.0 for s in adjusted_samples):
             print("  WARNING: Adjusted track might be clipping (samples hit max level)!")
        print()
        processed_tracks[name] = adjusted_samples

    print("--- Summary of Adjusted Loudness ---")
    for name, samples in processed_tracks.items():
        final_rms = calculate_rms_loudness(samples)
        print(f"  {name}: {final_rms:.3f}")

    print("\nThis simulation demonstrates how 'Auto Gain' aims to normalize the perceived loudness")
    print("of different audio tracks to a consistent target level, preventing sudden volume shifts.")
    print("In a real scenario, this would involve more complex audio analysis and processing.")