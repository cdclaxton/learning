// This code explores a mechanism by which the files in a folder can be
// fingerprinted to determine if the content is the same as that in a different
// folder.

package filechangedetection

import (
	"crypto/sha256"
	"fmt"
	"io"
	"log"
	"os"
	"path"
)

type FileSignatures map[string]string

// ChangeDetected returns true if the files in folder1 and folder2 differ.
func ChangeDetected(folder1 string, folder2 string) bool {

	// Generate the signatures of the files in the folders
	sig1 := generateSignatures(folder1)
	sig2 := generateSignatures(folder2)

	// Detect whether the file hashes are different
	return !signaturesSame(sig1, sig2)
}

func generateSignatures(filepath string) FileSignatures {

	sig := FileSignatures{}

	entries, err := os.ReadDir(filepath)
	if err != nil {
		log.Fatal(err)
	}

	for _, e := range entries {
		fmt.Printf("Generating signature of %s\n", e.Name())
		sig[e.Name()] = hashFile(filepath, e.Name())
	}

	return sig
}

func hashFile(folder string, filename string) string {
	f, err := os.Open(path.Join(folder, filename))
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	h := sha256.New()
	if _, err := io.Copy(h, f); err != nil {
		log.Fatal(err)
	}

	return fmt.Sprintf("%x", h.Sum(nil))
}

// signaturesSame returns true if the two file signatures are identical.
func signaturesSame(sig1 FileSignatures, sig2 FileSignatures) bool {

	if len(sig1) != len(sig2) {
		return false
	}

	for filename, hash1 := range sig1 {
		hash2, found := sig2[filename]
		if !found {
			return false
		}

		if hash1 != hash2 {
			return false
		}
	}

	return true
}
