package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"os"
	"strconv"
	"strings"

	"golang.org/x/exp/maps"
)

// Data represents the input data to the graph computation. The underlying data
// structure is purposefully abstracted away to handle a variety of different
// data types, such as lists, sets, and graphs (DAGs).
type Data interface {
	NumberOfValues(string) int // How many of the required value are in the data?
	Count() int
}

// SimpleData implements the Data interface.
type SimpleData struct {
	values []string
}

func NewSimpleData() *SimpleData {
	return &SimpleData{
		values: []string{},
	}
}

func NewPopulatedSimpleData(vals ...string) *SimpleData {
	sd := NewSimpleData()
	sd.AddValues(vals...)
	return sd
}

func (s *SimpleData) AddValues(vals ...string) {
	s.values = append(s.values, vals...)
}

func (s *SimpleData) NumberOfValues(val string) int {
	num := 0
	for _, value := range s.values {
		if value == val {
			num += 1
		}
	}
	return num
}

func (s *SimpleData) Count() int {
	return len(s.values)
}

func (s *SimpleData) String() string {
	return fmt.Sprintf("SimpleData(values = %v)", s.values)
}

// Computation defines a mapping from input values to an output value.
type Computation interface {
	Calculate([]int) (int, error) // Calculate output given inputs
	GetName() string              // Descriptive name for the computation
	String() string               // String representation of the node
}

// Computation types
const (
	AddComputation      = "Add"
	MultiplyComputation = "Multiply"
)

type AddValues struct{}

func (a AddValues) Calculate(values []int) (int, error) {
	total := 0
	for _, v := range values {
		total += v
	}
	return total, nil
}

func (a AddValues) GetName() string {
	return "Add"
}

func (a AddValues) String() string {
	return fmt.Sprintf("Computation(type=%s)", a.GetName())
}

type MultiplyValues struct{}

func (m MultiplyValues) Calculate(values []int) (int, error) {
	total := 1
	for _, v := range values {
		total *= v
	}
	return total, nil
}

func (m MultiplyValues) GetName() string {
	return "Multiply"
}

func (m MultiplyValues) String() string {
	return fmt.Sprintf("Computation(type=%s)", m.GetName())
}

// Extractor extracts an integer value from the Data.
type Extractor interface {
	Calculate(Data) (int, error)
	Instantiate(map[string]string) error
	String() string
}

type BaseExtractor struct {
	extractorType string
}

func (b *BaseExtractor) checkConfigType(config map[string]string) error {
	tpe, found := config[ExtractorType]
	if !found {
		return ErrExtractorConfigMissingType
	}

	if tpe != b.extractorType {
		return fmt.Errorf("%w: %v", ErrInstantiatingWrongType, tpe)
	}

	return nil
}

const (
	ExtractorType          = "type"               // Extractor type
	ConstantExtractor      = "ConstantExtractor"  // Extractor name for ExtractConstant
	NumValuesExtractor     = "NumValuesExtractor" // Extractor name for ExtractNumValues
	ExtractorValue         = "value"              // Extractor value for ExtractNumValues
	ConstantExtractorValue = "value"              // Extractor field name
	CountExtractor         = "CountExtractor"     // Extractor name for ExtractCount
)

type ExtractConstant struct {
	BaseExtractor
	value int
}

func NewExtractConstant() *ExtractConstant {
	return &ExtractConstant{
		BaseExtractor: BaseExtractor{
			extractorType: ConstantExtractor,
		},
	}
}

func (e *ExtractConstant) Instantiate(config map[string]string) error {

	err := e.checkConfigType(config)
	if err != nil {
		return err
	}

	value, found := config[ConstantExtractorValue]
	if !found {
		return ErrValueAttributeNotPresent
	}

	e.value, err = strconv.Atoi(value)
	return err

}

func (e *ExtractConstant) Calculate(data Data) (int, error) {
	return e.value, nil
}

func (e *ExtractConstant) String() string {
	return fmt.Sprintf("Extractor(type=%s, value=%d)", e.extractorType, e.value)
}

// ExtractNumValues is a type of Extractor.
type ExtractNumValues struct {
	BaseExtractor
	value string
}

func NewExtractNumValues() *ExtractNumValues {
	return &ExtractNumValues{
		BaseExtractor: BaseExtractor{
			extractorType: NumValuesExtractor,
		},
	}
}

func (e *ExtractNumValues) Instantiate(config map[string]string) error {

	err := e.checkConfigType(config)
	if err != nil {
		return err
	}

	value, found := config[ExtractorValue]
	if !found {
		return ErrValueAttributeNotPresent
	}

	e.value = value
	return nil
}

func (e *ExtractNumValues) Calculate(data Data) (int, error) {
	return data.NumberOfValues(e.value), nil
}

func (e *ExtractNumValues) String() string {
	return fmt.Sprintf("Extractor(type=%s, value=%s)", e.extractorType,
		e.value)
}

type ExtractCount struct {
	BaseExtractor
}

func NewExtractCount() *ExtractCount {
	return &ExtractCount{
		BaseExtractor: BaseExtractor{
			extractorType: CountExtractor,
		},
	}
}

func (e ExtractCount) Instantiate(config map[string]string) error {

	err := e.checkConfigType(config)
	if err != nil {
		return err
	}

	return nil
}

func (e *ExtractCount) Calculate(data Data) (int, error) {
	return data.Count(), nil
}

func (e *ExtractCount) String() string {
	return fmt.Sprintf("Extractor(type=%s)", e.extractorType)
}

var (
	ErrUnknownComputation         = errors.New("unknown type of computation")
	ErrNilComputeNode             = errors.New("compute node is nil")
	ErrExtractionConfigIsNil      = errors.New("extraction config is nil")
	ErrValueAttributeNotPresent   = errors.New("value attribute is not present")
	ErrUnknownExtractor           = errors.New("unknown type of extractor")
	ErrExtractorConfigMissingType = errors.New("type of extractor is missing from config")
	ErrInstantiatingWrongType     = errors.New("instantiating the wrong type of extractor")
	ErrNodeNameNotFound           = errors.New("node name not found")
	ErrInvalidGraph               = errors.New("invalid graph")
	ErrExtractorIsNil             = errors.New("extractor is nil")
	ErrComputationIsNil           = errors.New("computation is nil")
)

type Model struct {
	Nodes       []ComputeNode `json:"computeNodes"`
	Connections []Connection  `json:"connections"`
	outputNode  *ComputeNode  // Reference the final output node
}

func (m *Model) String() string {
	var sb strings.Builder
	sb.WriteString("Model(nodes=[")
	for idx, node := range m.Nodes {
		sb.WriteString(node.String())
		if idx < len(m.Nodes)-1 {
			sb.WriteString(", ")
		}
	}
	sb.WriteString("])")
	return sb.String()
}

// Compute the result of the model.
func (m *Model) Compute(data Data) (int, error) {
	return m.outputNode.Calculate(data)
}

type Connection struct {
	Source      string `json:"source"`      // Source (input)
	Destination string `json:"destination"` // Destination (output)
}

type ComputeNode struct {
	Name             string            `json:"name"`             // Typically a unique identifier for the node
	TakesData        bool              `json:"takesData"`        // Does the node take data or use values from parents?
	ComputationType  string            `json:"computationType"`  // Type of computation to perform (doesn't take data)
	ExtractionConfig map[string]string `json:"extractionConfig"` // Config for the extraction to perform (takes data)
	computation      Computation       // Computation to perform on the inputs
	extractor        Extractor         // Extractor that processes Data
	inputs           []*ComputeNode    // Input nodes to the compute node
}

func NewComputeNode(name string, takesData bool, computationType string,
	extractionConfig map[string]string) *ComputeNode {

	return &ComputeNode{
		Name:             name,
		TakesData:        takesData,
		ComputationType:  computationType,
		ExtractionConfig: extractionConfig,
		computation:      nil,
		extractor:        nil,
		inputs:           []*ComputeNode{},
	}
}

func (c *ComputeNode) AddInput(node *ComputeNode) error {
	if c == nil {
		return ErrNilComputeNode
	}

	c.inputs = append(c.inputs, node)
	return nil
}

// Instantiate either an extractor or a computation engine.
func (c *ComputeNode) Instantiate() error {

	if c.TakesData {
		return c.InstantiateExtractor()
	} else {
		return c.InstantiateComputation()
	}
}

// InstantiateComputation instantiates the computation engine within the node.
func (c *ComputeNode) InstantiateComputation() error {
	switch c.ComputationType {
	case AddComputation:
		c.computation = AddValues{}
	case MultiplyComputation:
		c.computation = MultiplyValues{}
	default:
		return fmt.Errorf("%w: %v", ErrUnknownComputation, c.ComputationType)
	}

	return nil
}

// InstantiateExtractor instantiates the extractor within the node.
func (c *ComputeNode) InstantiateExtractor() error {

	if c.ExtractionConfig == nil {
		return ErrExtractionConfigIsNil
	}

	extractorType, found := c.ExtractionConfig[ExtractorType]
	if !found {
		return ErrExtractorConfigMissingType
	}

	switch extractorType {

	case ConstantExtractor:
		c.extractor = NewExtractConstant()
	case NumValuesExtractor:
		c.extractor = NewExtractNumValues()
	case CountExtractor:
		c.extractor = NewExtractCount()
	default:
		return ErrUnknownExtractor
	}

	return c.extractor.Instantiate(c.ExtractionConfig)
}

// getInputValues to the compute node.
func (c *ComputeNode) getInputValues(data Data) ([]int, error) {
	result := make([]int, len(c.inputs))
	var err error

	for idx, inputNode := range c.inputs {
		result[idx], err = inputNode.Calculate(data)
		if err != nil {
			return nil, err
		}
	}

	return result, nil
}

func (c *ComputeNode) Calculate(data Data) (int, error) {

	if c.TakesData {
		if c.extractor == nil {
			return 0, fmt.Errorf("%w: node %v", ErrExtractorIsNil, c.Name)
		}
		return c.extractor.Calculate(data)
	}

	values, err := c.getInputValues(data)
	if err != nil {
		return 0, err
	}
	if c.computation == nil {
		return 0, fmt.Errorf("%w: node %v", ErrComputationIsNil, c.Name)
	}

	return c.computation.Calculate(values)
}

func (c *ComputeNode) String() string {
	if c.TakesData {
		return fmt.Sprintf("Node(name=%s, %s)", c.Name, c.extractor)
	}

	var sb strings.Builder
	for idx, n := range c.inputs {
		sb.WriteString(n.Name)
		if idx < len(c.inputs)-1 {
			sb.WriteString(", ")
		}
	}

	return fmt.Sprintf("Node(name=%s, %s, inputs=[%s])", c.Name, c.computation,
		sb.String())
}

// outputNode (or final node) given the connections.
func outputNode(connections []Connection) (string, error) {

	allNodes := map[string]bool{}
	seenAsSource := map[string]bool{}

	for _, connection := range connections {
		allNodes[connection.Source] = true
		allNodes[connection.Destination] = true

		seenAsSource[connection.Source] = true
	}

	outputNodes := map[string]bool{}

	for node := range allNodes {
		_, found := seenAsSource[node]
		if !found {
			outputNodes[node] = true
		}
	}

	if len(outputNodes) != 1 {
		return "", ErrInvalidGraph
	}

	return maps.Keys(outputNodes)[0], nil
}

// Load a model from a JSON file.
func LoadModel(filepath string) (*Model, error) {

	// Read the contents of the JSON file
	file, err := os.Open(filepath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	content, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}

	// Unmarshall the data
	var model Model
	err = json.Unmarshal(content, &model)
	if err != nil {
		return nil, err
	}

	// Instantiate the nodes within the model
	nameToIndex := map[string]int{}
	for idx := range model.Nodes {

		n := &model.Nodes[idx]
		if err := n.Instantiate(); err != nil {
			return nil, err
		}
		nameToIndex[n.Name] = idx
	}

	// Connect the nodes
	for _, conn := range model.Connections {
		srcIndex, found := nameToIndex[conn.Source]
		if !found {
			return nil, fmt.Errorf("%w: source %v", ErrNodeNameNotFound, conn.Source)
		}

		dstIndex, found := nameToIndex[conn.Destination]
		if !found {
			return nil, fmt.Errorf("%w: destination %v", ErrNodeNameNotFound, conn.Destination)
		}

		model.Nodes[dstIndex].AddInput(&model.Nodes[srcIndex])
	}

	// Store the reference to the final output node
	outputNodeName, err := outputNode(model.Connections)
	if err != nil {
		return nil, err
	}

	model.outputNode = &model.Nodes[nameToIndex[outputNodeName]]

	return &model, nil
}

func main() {
	fmt.Println("Graph defined computation")

	filepath := "./test-data/config-2.json"
	fmt.Printf("Reading model from file %s\n", filepath)

	model, err := LoadModel(filepath)
	if err != nil {
		log.Panic(err)
	}

	fmt.Println(model.String())

	sd := NewPopulatedSimpleData("a", "a", "b")
	result, err := model.Compute(sd)
	if err != nil {
		log.Panic(err)
	}
	fmt.Printf("Result = %d\n", result)
}
