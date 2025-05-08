package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var roundNumber bool

var addCmd = &cobra.Command{
	Use:     "add",
	Aliases: []string{"addition"}, // Array of alternative texts to invoke command
	Short:   "Add 2 numbers",
	Long:    "Add 2 numbers together",
	Args:    cobra.ExactArgs(2), // Constraints (exactly 2)
	Run: func(cmd *cobra.Command, args []string) {
		total, err := Add(args[0], args[1], roundNumber)
		if err != nil {
			fmt.Printf("Error adding %s and %s\n", args[0], args[1])
		} else {
			fmt.Printf("%s + %s = %f\n", args[0], args[1], total)
		}
	},
}

func init() {
	// Add the boolean flag to denote that the number should be rounded
	addCmd.Flags().BoolVarP(&roundNumber, "round", "r", false, "round to the nearest integer")

	// The add command is added as a subcommand of the root
	rootCmd.AddCommand(addCmd)
}
