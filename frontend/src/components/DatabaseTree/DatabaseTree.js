import React from "react";
import { ListGroup } from "react-bootstrap";

const TreeNode = ({ node }) => {
  if (!node.children || node.children.length === 0) {
    // Si el nodo no tiene hijos, solo muestra el nombre
    return <ListGroup.Item>{node.name}</ListGroup.Item>;
  }

  // Si el nodo tiene hijos, renderiza un elemento de lista y recursivamente renderiza los hijos
  return (
    <ListGroup.Item>
      {node.name}
      <ListGroup>
        {node.children.map((childNode, index) => (
          <TreeNode key={index} node={childNode} />
        ))}
      </ListGroup>
    </ListGroup.Item>
  );
};

const DatabaseTree = () => {
  const data = [
    {
      name: "Base de Datos 1",
      children: [
        {
          name: "Tablas",
          children: [
            { name: "Tabla1" },
            { name: "Tabla2" }
          ]
        },
        {
          name: "Procedimientos",
          children: [
            { name: "Procedimiento1" },
            { name: "Procedimiento2" }
          ]
        },
        {
          name: "Funciones",
          children: [
            { name: "Funcion1" },
            { name: "Funcion2" }
          ]
        }
      ]
    },
    // {
    //   name: "Base de Datos 2",
    //   children: [
    //     {
    //       name: "Tablas",
    //       children: [
    //         { name: "Tabla1" },
    //         { name: "Tabla2" }
    //       ]
    //     },
    //     {
    //       name: "Procedimientos",
    //       children: [
    //         { name: "Procedimiento1" },
    //         { name: "Procedimiento2" }
    //       ]
    //     },
    //     {
    //       name: "Funciones",
    //       children: [
    //         { name: "Funcion1" },
    //         { name: "Funcion2" }
    //       ]
    //     }
    //   ]
    // },
    // Agrega más bases de datos según sea necesario
    // ...
  ];

  return (
    <div className="col-2 py-4">
      <ListGroup>
        {data.map((node, index) => (
          <TreeNode key={index} node={node} />
        ))}
      </ListGroup>
    </div>
  );
};

export default DatabaseTree;
