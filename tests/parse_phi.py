import re
import statistics

def process_phi_logs(file_path):
    initial_phis = []
    final_phis = []
    differences = []
    
    current_run = None
    current_initial_phi = None
    current_final_phi = None
    
    with open(file_path, 'r') as file:
        for line in file:
            # Check for a new run
            run_match = re.search(r'\[INFO\] run:\s+(\d+)', line)
            if run_match:
                # If moving to a new run, store the completed run's data
                if current_run is not None:
                    initial_phis.append(current_initial_phi)
                    final_phis.append(current_final_phi)
                    differences.append(current_final_phi - current_initial_phi)
                
                # Reset for the new run
                current_run = int(run_match.group(1))
                current_initial_phi = None
                current_final_phi = None
                continue
                
            # Check for a phi value
            phi_match = re.search(r'\[INFO\] phi:\s+([0-9.]+)', line)
            if phi_match and current_run is not None:
                phi_value = float(phi_match.group(1))
                
                # If this is the first phi seen in this run, set it as initial
                if current_initial_phi is None:
                    current_initial_phi = phi_value
                
                # Continuously overwrite the final phi until the run ends
                current_final_phi = phi_value
                
        # Append the final run's data after reaching the end of the file
        if current_run is not None and current_initial_phi is not None and current_final_phi is not None:
            initial_phis.append(current_initial_phi)
            final_phis.append(current_final_phi)
            differences.append(current_final_phi - current_initial_phi)
            
    # Calculate the median of the differences
    median_difference = statistics.median(differences) if differences else 0
    
    return initial_phis, final_phis, differences, median_difference

# --- Execution ---
if __name__ == "__main__":
    # Replace 'log_file.txt' with the actual path to your attached file
    file_path = '/home/benjamin_faught/Pivoting-Cube-Reconfiguration/test_models/stage_n10/testing_sb3.log' 
    
    try:
        initial_list, final_list, diff_list, median_diff = process_phi_logs(file_path)
        
        print(f"Initial Phi Values: {initial_list}")
        print(f"Final Phi Values: {final_list}")
        print(f"Differences (Final - Initial): {diff_list}")
        print(f"Median Phi Difference: {median_diff}")
        
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")