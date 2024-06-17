package server

import (
	"fmt"
	"io"
	"net"
	"sync"
	"time"

	"github.com/cdclaxton/protobuf-example/messages"
	"google.golang.org/protobuf/proto"
)

type Server struct {
	ListenAddress string
	listener      net.Listener
	wg            sync.WaitGroup
	requestStop   chan bool
}

func NewServer(ListenAddress string) *Server {
	return &Server{
		ListenAddress: ListenAddress,
		requestStop:   make(chan bool),
	}
}

func (s *Server) Start() error {

	// Setup the TCP listener
	var err error
	s.listener, err = net.Listen("tcp", s.ListenAddress)
	if err != nil {
		return err
	}

	s.wg.Add(1)
	go s.serve()
	return nil
}

func (s *Server) serve() {
	defer s.wg.Done()

	for {
		conn, err := s.listener.Accept()
		if err != nil {
			select {
			case <-s.requestStop:
				return
			default:
				fmt.Printf("Listener accept error: %v\n", err)
				return
			}
		}

		s.wg.Add(1)
		go func() {
			s.handle(conn)
			s.wg.Done()
		}()
	}
}

func (s *Server) handle(conn net.Conn) {
	defer conn.Close()

	bytes, err := io.ReadAll(conn)
	if err != nil {
		fmt.Printf("handle() error: %v\n", err)
		return
	}

	fmt.Printf("handle(): received %d bytes\n", len(bytes))

	var msg messages.Message
	if err := proto.Unmarshal(bytes, &msg); err != nil {
		fmt.Printf("handle(): error: %v\n", err)
		return
	}

	content := msg.GetContent()
	switch msg := content.(type) {
	case *messages.Message_Registration:
		s.handleRegistration(msg.Registration)
	case *messages.Message_Status:
		s.handleStatus(msg.Status)
	}
}

func (s *Server) handleRegistration(msg *messages.Registration) {
	fmt.Printf("Received registration: id=%d, time=%v\n",
		msg.Id, msg.Time.AsTime().Format(time.RFC1123Z))
}

func (s *Server) handleStatus(msg *messages.Status) {
	fmt.Printf("Received status message: sender=%d, status=%v, time=%v\n",
		msg.Sender, msg.Status, msg.Time.AsTime().Format(time.RFC1123Z))
}

func (s *Server) Stop() {
	close(s.requestStop)
	s.listener.Close()

	// Wait until all connections are closed
	s.wg.Wait()
}
