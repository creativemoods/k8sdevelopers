FROM golang:1.16 AS builder
WORKDIR /go/src/training/helloworld/
RUN go mod init
COPY app.go ./
COPY entrypoint.sh ./
RUN CGO_ENABLED=0 go build -a -installsuffix cgo -o app .

FROM alpine:latest  
WORKDIR /root/
COPY --from=builder /go/src/training/helloworld/app ./
COPY --from=builder /go/src/training/helloworld/entrypoint.sh ./
RUN chmod 755 /root/entrypoint.sh
ENTRYPOINT ["/root/entrypoint.sh"]
CMD ["./app"]
