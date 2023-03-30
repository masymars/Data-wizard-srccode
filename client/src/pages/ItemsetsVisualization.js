import React, { useState, useEffect } from 'react';
import {Tree} from 'react-tree-graph';
import 'react-tree-graph/dist/style.css'
// Function to convert itemsets data to tree data format
const convertItemsetsToTreeData = (itemsets) => {
    const tree = { name: 'Root', children: [] };
  
    itemsets.forEach((itemset) => {
      let currentNode = tree;
  
      itemset.itemset.forEach((item) => {
        let childNode = currentNode.children.find(
          (child) => child.name === item
        );
  
        if (!childNode) {
          childNode = { name: item, children: [] };
          currentNode.children.push(childNode);
        }
  
        currentNode = childNode;
      });
    });
  
    return tree;
  };
  
  const getNumberOfItems = (itemsets) => {
    const items = new Set();
    itemsets.forEach((itemset) => {
      itemset.itemset.forEach((item) => items.add(item));
    });
    return items.size;
  };
  
  const getMaxDepth = (tree) => {
    if (tree.children.length === 0) return 0;
    return 1 + Math.max(...tree.children.map(getMaxDepth));
  };
  
  const ItemsetsVisualization = ({ returnedData }) => {
    const [treeData, setTreeData] = useState({ name: 'Root', children: [] });
  
    // Call this function when you receive the itemsets data from the server
    const handleReturnedData = (returnedData) => {
      setTreeData(convertItemsetsToTreeData(returnedData));
    };
  
    // Call handleReturnedData when you receive the returnedData
    useEffect(() => {
      handleReturnedData(returnedData);
    }, [returnedData]);
  
    const width = getNumberOfItems(returnedData) * 100;
    const height = getMaxDepth(treeData) * 100;
  
    return (
      <div className='tree-divs'>
        <Tree
          data={treeData}
          height={height}
          width={400}
          svgProps={{
            transform: 'rotate(90)',
          }}
          textProps={{
            transform: 'rotate(-45)',
            style: {
              fontSize: '12px', // Adjust the font size here
            },
          }}
          animated
        />
      </div>
    );
  };
  
  export default ItemsetsVisualization;