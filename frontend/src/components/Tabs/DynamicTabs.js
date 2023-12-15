// DynamicTabs.js (Componente DynamicTabs)
import React, { useState, forwardRef, useImperativeHandle } from "react";
import { Tab, Tabs, Button } from "react-bootstrap";
import ConsoleIn from "../Editor/ConsoleIn";

const DynamicTabs = forwardRef((props, ref) => {
  const [key, setKey] = useState("query1");
  const [tabs, setTabs] = useState([
    { key: "query1", title: "Query 1", content: "Contenido de la pestaña 1" },
  ]);

  const addTab = () => {
    const newKey = `query${tabs.length + 1}`;
    const newTab = { key: newKey, title: `Query ${tabs.length + 1}`, content: `Contenido de la pestaña ${tabs.length + 1}` };
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

  const handleExecuteQuery = () => {
        
  }


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
                <ConsoleIn onExecuteQuery={ () => handleExecuteQuery2(tab.key)}/>
              </Tab>
            ))}
          </Tabs>
        </div>
      </div>
    </div>
  );
});

export default DynamicTabs;
