package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "zero",                                                            // Text used to invoke the command
	Short: "zero performs basic mathematical operations",                     // Short description
	Long:  "zero performs basic mathematical operations -- add and subtract", // Long description
	Run: func(cmd *cobra.Command, args []string) { // Function to be executed on invocation
		fmt.Println("Root")
	},
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
