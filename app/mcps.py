from fastmcp import FastMCP, FastMCPApp
from prefab_ui.app import PrefabApp
from prefab_ui.actions import ShowToast
from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import Button, Card, CardContent, Column, Heading, Text

app = FastMCPApp("toolsui")


@app.tool()
def process_payment(amount: str) -> str:
    """Payment process karne wala backend tool."""
    return f"Payment of Rs. {amount} Successful!"


@app.ui()
def show_payment_screen(amount: str = "500") -> PrefabApp:
    """Payment UI screen"""

    with Column(gap=4, css_class="p-6") as view:
        with Card():
            with CardContent():
                Heading("FastMCP Payment Gateway")
                Text(f"Do you want to pay Rs. {amount} now?")

                Button(
                    "Pay Now",
                    on_click=[
                        CallTool(
                            process_payment,
                            arguments={"amount": amount},
                            on_success=ShowToast(
                                "Payment Processed!",
                                variant="success",
                            ),
                        ),
                    ],
                )

    return PrefabApp(view=view)


mcp = FastMCP("My Assistant Tools", providers=[app])

@mcp.tool
def get_weather(city: str) -> str:
    """Return the requested city name."""
    return f"The city name is {city}."




if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)



