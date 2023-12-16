import React from "react";
import { Card, Accordion } from "react-bootstrap";

function TreeNode ({ node }){
  if (!node.children || node.children.length === 0) {
    return <Card.Body>{node.name}</Card.Body>;
  }

  const cardData = () => (
    <Card>
      <Accordion.Toggle as={Card.Header} eventKey={node.name}>
        {node.name}
      </Accordion.Toggle>
      <Accordion.Collapse eventKey={node.name}>
        <Card.Body>
          {node.children.map((childNode, index) => (
            <TreeNode key={index} node={childNode} />
          ))}
        </Card.Body>
      </Accordion.Collapse>
    </Card>
  );

  return cardData;
};

export default TreeNode;
