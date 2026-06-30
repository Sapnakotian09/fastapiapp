import { useState } from "react";

function Welcome() {
    const [count, setCount] = useState(0);
    const increment = () => {
        setCount((current) => current + 1);
    };

    return (
        <section className="hero">
            <div className="hero-card">
                <h1>Count: {count}</h1>
                <button className="counter" onClick={increment}>Increment</button>
            </div>
        </section>
    );
}

export default Welcome