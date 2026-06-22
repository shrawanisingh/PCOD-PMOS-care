import os
import argparse


def main():
	parser = argparse.ArgumentParser(description="Run the PCOD-PMOS agent pipeline")
	parser.add_argument("--mock", action="store_true", help="Enable mock LLM responses (MOCK_LLM=1)")
	parser.add_argument("--query", "-q", type=str, help="Provide patient query non-interactively")
	args = parser.parse_args()

	if args.mock:
		os.environ["MOCK_LLM"] = "1"

	from agents.clinical import run_clinical
	from agents.metabolic import run_metabolic
	from agents.lifestyle import run_lifestyle
	from agents.planner import run_planner

	if args.query:
		query = args.query
	else:
		query = input("Describe your symptoms: ")

	print("\nRunning Clinical Agent...")
	clinical = run_clinical(query)

	print("\nRunning Metabolic Agent...")
	metabolic = run_metabolic(query)

	print("\nRunning Lifestyle Agent...")
	lifestyle = run_lifestyle(query)

	combined = f"""
CLINICAL:
{clinical}

METABOLIC:
{metabolic}

LIFESTYLE:
{lifestyle}
"""

	print("\nGenerating Final Report...")

	final_report = run_planner(combined)

	print("\n========== FINAL REPORT ==========")
	print(final_report)


if __name__ == "__main__":
	main()