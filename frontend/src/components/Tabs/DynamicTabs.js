import React, { useState, forwardRef, useImperativeHandle } from "react";
import { Tab, Tabs, Button } from "react-bootstrap";
import { Editor } from "@monaco-editor/react";

const DynamicTabs = forwardRef((props, ref) => {
  const [key, setKey] = useState("query1");
  const [tabs, setTabs] = useState([
    { key: "query1", title: "Query 1", content: "Contenido de la pestaña 1" },
  ]);

  const addTab = () => {
    const newKey = `query${tabs.length + 1}`;
    const newTab = { key: newKey, title: `Query ${tabs.length + 1}`, content: '' }; // Inicializamos con cadena vacía
    setTabs([...tabs, newTab]);
    setKey(newKey);
};

  const removeTab = (tabKey) => {
    const updatedTabs = tabs.filter((tab) => tab.key !== tabKey);
    setTabs(updatedTabs);
    setKey(updatedTabs.length > 0 ? updatedTabs[0].key : null);
  };

  // Exponer la función addTab mediante useImperativeHandle
  useImperativeHandle(ref, () => ({
    addTab: addTab,
    handleExecuteQuery2: handleExecuteQuery2,
  }));

  const handleExecuteQuery2 = () => {
    // Puedes realizar alguna lógica específica aquí, si es necesario
    console.log(`Ejecutando consulta para la pestaña `);
  };

  return (
    <div className='col-10'>
      <div className='row'>
        <div className='py-4'>
          <Tabs activeKey={key} onSelect={(k) => setKey(k)}>
            {tabs.map((tab) => (
              <Tab key={tab.key} eventKey={tab.key} title={(
                <span style={{ position: "relative" }}>
                  {tab.title}{" "}
                  <Button variant="link" onClick={() => removeTab(tab.key)} style={{ position: "relative", top: -10, left: 15, color: "red" }}>
                    x
                  </Button>
                </span>
              )}>
                {/* Editor de texto, salida y consola */}
                <div className='container-fluid'>
                  <div className='row '>
                    <div className='col-6 py-1'>
                      <h5>Editor</h5>
                      <Editor
                        width='100%'
                        height='500px'
                        language='sql'
                        theme='vs-dark'
                        value={props.sqlContent[tab.key] || ''} // Asociamos el contenido de la pestaña
                      />
                    </div>
                    <div className='col-6 py-1'>
                      <h5>Salida</h5>
                      <Editor
                        width='100%'
                        height='500px'
                        language='plaintext'
                        theme='vs-dark'
                        options={{
                          readOnly: true,
                          wordWrap: 'on',
                        }}
                        // value={queryResult}
                      />
                    </div>
                    <div className='col-12 '>
                      <h5>Consola</h5>
                      <Editor
                        width='100%'
                        height='200px'
                        language='plaintext'
                        theme='vs-dark'
                        options={{
                          readOnly: true,
                          wordWrap: 'on',
                        }}
                      />
                    </div>
                  </div>
                </div>
              </Tab>
            ))}
          </Tabs>
        </div>
      </div>
    </div>
  );
});

export default DynamicTabs;