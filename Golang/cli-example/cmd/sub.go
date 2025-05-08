package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var subCmd = &cobra.Command{
	Use:     "sub",
	Aliases: []string{"subtract"}, // Array of alternative texts to invoke command
	Short:   "Subtract 2 numbers",
	Long:    "Subtract 2 numbers",
	Args:    cobra.ExactArgs(2), // Constraints (exactly 2)
	Run: func(cmd *cobra.Command, args []string) {
		total, err := Subtract(args[0], args[1], roundNumber)
		if err != nil {
			fmt.Printf("Error adding %s and %s\n", args[0], args[1])
		} else {
			fmt.Printf("%s + %s = %f\n", args[0], args[1], total)
		}
	},
}

func init() {
	// Add the boolean flag to denote that the number should be rounded
	subCmd.Flags().BoolVarP(&roundNumber, "round", "r", false, "round to the nearest integer")

	// The sub command is added as a subcommand of the root
	rootCmd.AddCommand(subCmd)
}
