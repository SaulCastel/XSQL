import DropdownButton from 'react-bootstrap/DropdownButton';
import Dropdown from 'react-bootstrap/Dropdown';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Button from 'react-bootstrap/esm/Button';
import ButtonToolbar from 'react-bootstrap/ButtonToolbar';

function Tools() {
    return (
        <div className="container-fluid bg-info">
            <div className="container py-2">
                <ButtonToolbar aria-label="Toolbar with button groups">
                    <ButtonGroup className="me-2">
                        <DropdownButton as={ButtonGroup} title="Base de datos" id="bg-nested-dropdown" variant="warning">
                            <Dropdown.Item eventKey="1">Nueva base de datosk</Dropdown.Item>
                            <Dropdown.Item eventKey="2">Eliminar base de datos</Dropdown.Item>
                            <Dropdown.Item eventKey="3">Crear DUMP</Dropdown.Item>
                            <Dropdown.Item eventKey="4">Seleccionar base de datos</Dropdown.Item>
                        </DropdownButton>
                    </ButtonGroup>
                    <ButtonGroup className="me-2">
                        <DropdownButton as={ButtonGroup} title="SQL" id="bg-nested-dropdown" variant="warning">
                            <Dropdown.Item eventKey="1">Nuevo Query</Dropdown.Item>
                            <Dropdown.Item eventKey="2">Ejecutar Query</Dropdown.Item>
                        </DropdownButton>
                    </ButtonGroup>
                    <ButtonGroup className="me-2">
                        <Button variant="warning">
                            IMPORTAR
                        </Button>
                    </ButtonGroup>
                    <ButtonGroup className="me-2">
                        <Button variant="warning">
                            EXPORTAR
                        </Button>
                    </ButtonGroup>
                </ButtonToolbar>
            </div>

        </div>
    );
}

export default Tools;