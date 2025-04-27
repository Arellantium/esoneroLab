import React, { useState } from 'react';
import { Container, Tabs, Tab, Form, Button, ListGroup, Table} from 'react-bootstrap';

function Dashboard() {

  const [messaggio, setDomanda] = useState('');
  const [nomiRegisti, setNomiRegisti] = useState([]);
  const [validatedSearch, setValidatedSearch] = useState(false);
  const [validatedAdd, setValidatedAdd] = useState(false);
  const [richiesta, setRichiesta] = useState('');
  const [csvData, setCsvData] = useState('');
  const [ottieniSchema, setOttieniSchema] = useState('');
  const [erroreApiDomanda, setErroreApiDomanda] = useState('');

  const inviaDomanda = async (e) => {
    
    e.preventDefault(); 

    if (messaggio.trim() === '') {
      setValidatedSearch(true);
      return;
    }
  
    setValidatedSearch(false);  
    
    try {
      const response = await fetch(`http://127.0.0.1:8005/search/${encodeURIComponent(messaggio)}`);
      if (response.ok) {
        const data = await response.json();
        console.log('Risposta dal server:', data);

        // Estrai solo i "name" da ogni item
        const nomi = data.map(item => {
          const nomeProperty = item.properties.find(prop => prop.property_name === 'name');
          return nomeProperty ? nomeProperty.property_value : '';
        }).filter(nome => nome !== ''); // Rimuovi eventuali vuoti

        setNomiRegisti(nomi);
    }else if (response.status === 422) {
      const errorData = await response.json();
      console.log('Errore 422:', errorData);

      const errorMessage = errorData.detail.errore;
      const suggerimenti = errorData.detail.possibili_domande;

      setErroreApiDomanda([
        <>
          <div className="alert alert-danger text-start mt-3"  role="alert">
            {errorMessage}
            <ul className="mt-3">
              {suggerimenti.map((domanda, index) => (
                <li key={index}>{domanda}</li>
              ))}
            </ul>
          </div>
        </>
      ]);
    } else {
      setErroreApiDomanda(['Errore sconosciuto.']);
    }
  } catch (error) {
    console.error('Errore nella richiesta:', error);
    setNomiRegisti([]);
  }
};

const inviaFilm = async (e) => {

  e.preventDefault(); 

    if (csvData.trim() === '') {
      setValidatedAdd(true);
      return;
    }
  
    setValidatedAdd(false);  

  try {
    const response = await fetch('http://127.0.0.1:8005/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ riga_csv: csvData })
    });

    if (response.ok) {
      setRichiesta('Inserimento riuscito con successo!');
      setCsvData(''); // Puliamo l'input dopo inserimento
    } else {
      setRichiesta('Errore durante l\'inserimento.');
    }
  } catch (error) {
    console.error('Errore:', error);
    setRichiesta('Errore di connessione con il server.');
  }
};

  const inviaOttieniSchema = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8005/schema_summary');
      const data = await response.json();
      console.log('Schema ricevuto:', data);
      setOttieniSchema(data);
    } catch (error) {
      console.error('Errore durante il recupero dello schema:', error);
      setOttieniSchema([]);
    }
  };
  
  

  return (
    <Container className="mt-5">
    <Tabs
      defaultActiveKey="home"
      id="tabs-example"
      className="mb-3"
      fill
    >
      <Tab eventKey="home" title={<><i className="fas fa-magnifying-glass"></i> Search</>}>
        <h3>Search</h3>
        <p>
          <Form noValidate validated={validatedSearch} onSubmit={inviaDomanda}>
            <Form.Group controlId="formDomanda">
              <Form.Label>Fai una domanda</Form.Label>
              <Form.Control 
                type="text" 
                placeholder="Scrivi qui la tua domanda" 
                value={messaggio}
                onChange={(e) => setDomanda(e.target.value)}
                required
                isInvalid={validatedSearch && messaggio.trim() === ''}
              />
              <Form.Control.Feedback type="invalid">
                Il campo domanda è obbligatorio.
              </Form.Control.Feedback>
            </Form.Group>
            <Button variant="primary" className="mt-3" onClick={inviaDomanda}>
              Invia
            </Button>
          </Form>

           {/* Qui mostriamo la lista dei registi */}
           {nomiRegisti.length > 0 && (
            <ListGroup className="mt-4">
              {nomiRegisti.map((nome, index) => (
                <ListGroup.Item key={index}>
                  {nome}
                </ListGroup.Item>
              ))}
            </ListGroup>
          )}

              {erroreApiDomanda && (
            <div className="alert-danger" role="alert">
              {erroreApiDomanda}
            </div>
          )}
        </p>
      </Tab>

      <Tab eventKey="profile" title={<><i className="fas fa-plus"></i> Add</>}>
        <h3>Aggiungi un film</h3>
        <p>
        <Form noValidate validated={validatedAdd} onSubmit={inviaFilm}>
            <Form.Group controlId="formDomanda">
              <Form.Label>inserisci il formato csv</Form.Label>
              <Form.Control 
                type="text" 
                placeholder="es: titolo,anno,regista,età,genere,piattaforma,piattaforma" 
                value={csvData}
                onChange={(e) => setCsvData(e.target.value)}
                required
                isInvalid={validatedAdd && csvData.trim() === ''}
              />
              <Form.Control.Feedback type="invalid">
                Il campo add è obbligatorio.
              </Form.Control.Feedback>
            </Form.Group>
            <Button variant="primary" className="mt-3" onClick={inviaFilm}>
              Invia
            </Button>
          </Form>
          {richiesta && (
            <div className={`mt-4 alert ${richiesta.includes('successo') ? 'alert-success' : 'alert-danger'}`} role="alert">
              {richiesta}
            </div>
          )}
        </p>
      </Tab>

      <Tab eventKey="contact" title={<><i className="fas fa-database"></i> Get Schema</>}>
        <h3>Ottieni lo schema</h3>
        <p>
          <Button variant="primary" className="mt-3" onClick={inviaOttieniSchema}>
            Ottieni Schema
          </Button>

          {/* Mostra la tabella se abbiamo dati */}
          {ottieniSchema.length > 0 && (
            <div className="mt-4">
              <h5>Schema delle Tabelle:</h5>
              <Table striped bordered hover responsive>
                <thead>
                  <tr>
                    <th>Tabella</th>
                    <th>Colonna</th>
                    <th>Campo</th>
                  </tr>
                </thead>
                <tbody>
                  {ottieniSchema.map((campo, index) => (
                    <tr key={index}>
                      <td>{campo.table_name}</td>
                      <td>{campo.column_name}</td>
                      <td>{campo.table_column}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
          )}
        </p>
      </Tab>
    </Tabs>
  </Container> 
  );
}

export default Dashboard;
