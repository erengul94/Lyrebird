

import { Container, Navbar, Nav, Button } from "react-bootstrap";


function CustomNavbar() {

    return (
        <>
            <Navbar bg="primary" variant="dark" expand="lg" className="shadow-sm">
                <Container>
                    <Navbar.Brand href="#home">
                        <img
                            src="/path/to/logo.png" // Add your logo image here
                            alt="Healthcare App Logo"
                            width="30"
                            height="30"
                            className="d-inline-block align-top"
                        />
                        Healthcare App
                    </Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="ms-auto">
                            <Nav.Link href="#home" className="hover-link">Home</Nav.Link>
                            <Nav.Link href="#patients" className="hover-link">Patients</Nav.Link>
                            <Nav.Link href="#records" className="hover-link">Records</Nav.Link>
                            <Nav.Link href="#about" className="hover-link">About</Nav.Link>
                        </Nav>
                        <Button variant="outline-light" className="ms-2">Login</Button>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </>
    )
}



export default CustomNavbar;