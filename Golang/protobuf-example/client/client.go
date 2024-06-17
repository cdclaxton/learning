package client

import (
	"net"

	"github.com/cdclaxton/protobuf-example/messages"
	"google.golang.org/protobuf/proto"
	"google.golang.org/protobuf/types/known/timestamppb"
)

type Client struct {
	Id                  int32
	serverListenAddress string
	conn                net.Conn
}

func NewClient(id int32, server string) *Client {
	return &Client{
		Id:                  id,
		serverListenAddress: server,
	}
}

func (c *Client) ConnectToServer() error {

	return nil
}

func (c *Client) sendMessage(msg []byte) error {
	tcpAddr, err := net.ResolveTCPAddr("tcp", c.serverListenAddress)
	if err != nil {
		return err
	}

	c.conn, err = net.DialTCP("tcp", nil, tcpAddr)
	if err != nil {
		return err
	}

	_, err = c.conn.Write(msg)
	if err != nil {
		return err
	}

	return c.conn.Close()
}

func (c *Client) SendRegistrationRequest() error {
	reg := messages.Registration{
		Id:   c.Id,
		Time: timestamppb.Now(),
	}

	msg := messages.Message{
		Time:   timestamppb.Now(),
		Sender: c.Id,
		Content: &messages.Message_Registration{
			Registration: &reg,
		},
	}

	out, err := proto.Marshal(&msg)
	if err != nil {
		return err
	}

	return c.sendMessage(out)
}

func (c *Client) SendStatus() error {
	status := messages.Status{
		Time:   timestamppb.Now(),
		Sender: c.Id,
		Status: messages.StatusType_STATUS_OK,
	}

	msg := messages.Message{
		Time:   timestamppb.Now(),
		Sender: c.Id,
		Content: &messages.Message_Status{
			Status: &status,
		},
	}

	out, err := proto.Marshal(&msg)
	if err != nil {
		return err
	}

	return c.sendMessage(out)
}
