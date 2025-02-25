import React, { useState } from "react";

function FilterSidebar() {
  const [isOpen, setIsOpen] = useState(false);
  const [filterData, setFilterData] = useState({})
  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };
  const updateFilters = (key, value) => {
    
  }
  return (
    <div>
      <button
        onClick={toggleSidebar}
        className=""
      >
        {isOpen ? "Close Filters" : "Open Filters"}
      </button>

      {/* Sidebar */}
      <div
        className=""
        
      >
        {/* Sidebar content */}
        <div className="">
          <h2 className="">Filter Watches</h2>
          <form>
            <div className="mb-4">
              <label className="">Name</label>
              <input
                type="text"
                placeholder="Name"
                className=""
              />
            </div>

            <div className="mb-4">
              <label className="">Brand</label>
              <select className="">
                <option value="">Select Brand</option>
                <option value="brand1">Brand 1</option>
                <option value="brand2">Brand 2</option>
              </select>
            </div>

            <div className="mb-4">
              <label className="">Min Price</label>
              <input
                type="number"
                placeholder="Min Price"
                className=""
              />
            </div>

            <div className="mb-4">
              <label className="">Max Price</label>
              <input
                type="number"
                placeholder="Max Price"
                className=""
              />
            </div>

            <div className="mb-4">
              <label className="">
                Min Water Resistance (m)
              </label>
              <input
                type="number"
                placeholder="Min Water Resistance"
                className=""
              />
            </div>

            <div className="mb-4">
              <label className="">Movement Type</label>
              <select className="">
                <option value="">Select Movement</option>
                <option value="automatic">Automatic</option>
                <option value="quartz">Quartz</option>
              </select>
            </div>

            <button
              type="submit"
              className=""
            >
              Apply Filters
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default FilterSidebar;
