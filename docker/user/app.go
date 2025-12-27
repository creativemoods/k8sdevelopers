package main
import "fmt"
import "log"
import "os/user"

func main() {
    user, err := user.Current()
    if err != nil {
        log.Fatalf(err.Error())
    }
    fmt.Printf("hello world from %s\n", user.Username)
}
