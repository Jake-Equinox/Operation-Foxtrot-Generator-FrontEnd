import streamlit as st

class StreamLit:

    def mainPage():
        st.title("Foxtrot Quote Generator 🦊")
        
        text = "Hey there 👋 This is an instant quote generator made from scratch by the Foxtrot Team!  \n \
              \n Fill out of the side bar on the left to get started. Press the '>' arrow if it's not there. \n \
              \n Please know that this is a work in progress and issues do occur. If they do, please email us at: FoxtrotPrints@gmail.com so we can squash any bugs 🪲  \n \
              \n **Final quote is subject to evaluation by the Foxtrot Team!**"

        st.info(text)

        st.markdown("---")

        with st.sidebar:
            numOfShirt = st.number_input("How many shirts?", min_value = 20, max_value = 250)
            cusSupply = st.radio("Are you supplying the garment?", ['No', 'Yes'])
            
            garmentCost = None
            if cusSupply == 'No':
                garmentCost = 10
            featuredArtist = st.radio("Have you completed a Featured Artist run before?", ['No', 'Yes'])
            numOfColour = st.slider("How many colours are present in your graphic?", max_value=3)
            whitePrint = st.radio("Is white a colour?", ['No','Yes'])
            
            whiteQuantity = None
            if whitePrint == 'Yes':
                whiteQuantity = st.slider("How many shirts require white ink?", max_value= numOfShirt)

            twoSides = st.radio("Is there a backgraphic?", ['No', 'Yes'])
            
            backNum = None
            if twoSides == 'Yes':
                backNum = st.slider("How many shirts require backgraphics?", max_value=numOfShirt)
            
            largeGraphic = st.radio("Is the print a large graphic (greater than 14.8 (W) x 21.0 (H) cm?", ['No', 'Yes'])
            screens = numOfColour
            addOns = st.multiselect("Are there any add ons?", options=['Puff Print', 'Neck Prints', 'Outsourced Labels'])        
        

        x, xy, w, g, c, s, addOnTotal, initialEquation, equation, discount = Utilities.calculateContractJob(cusSupply, featuredArtist, numOfShirt, garmentCost, numOfColour, 
                            whitePrint, whiteQuantity, twoSides, backNum, largeGraphic, screens, addOns)


        if numOfShirt == 0:
            st.error("Please complete sidebar before continuing!")
        else:
            st.write("")
            Utilities.printOut(cusSupply, featuredArtist, numOfShirt, garmentCost, x, xy, w, g, c, s, addOnTotal, initialEquation, equation, discount)
            Utilities.customerForm()


        

class Utilities:

    def calculateContractJob(cusSupply, featuredArtist, numOfShirt, garmentCost, numOfColour, 
                            whitePrint, whiteQuantity, twoSides, backNum, largeGraphic, screens, addOns):
        
        shirtBelow20 = 12
        shirt20_49 = 7
        shirt50_99 = 5.50
        shirt100_249 = 4
        shirt250_plus = 3
        
        
        twoSidesCost = 0
        if twoSides == 'Yes':
            twoSidesCost = 2

        x = 0
        if cusSupply == 'No':
            if numOfShirt < 20:
                x = (shirtBelow20 + twoSidesCost) + garmentCost
                xy = shirtBelow20
            elif numOfShirt >= 20 and numOfShirt <= 49:
                x = (shirt20_49 + twoSidesCost) + garmentCost
                xy = shirt20_49
            elif numOfShirt >= 50 and numOfShirt <= 99:
                x = (shirt50_99 + twoSidesCost) + garmentCost
                xy = shirt50_99
            elif numOfShirt >= 100 and numOfShirt <= 249:
                x = (shirt100_249 + twoSidesCost) + garmentCost
                xy = shirt100_249
            elif numOfShirt >= 250:
                x = (shirt250_plus + twoSidesCost) + garmentCost
                xy = shirt250_plus
        elif cusSupply == 'Yes':
            if numOfShirt < 20:
                print("Please double check with customer about printing less than 20!")
                x = (shirtBelow20 + twoSidesCost)
                xy = shirtBelow20
            elif numOfShirt >= 20 and numOfShirt <= 49:
                x = (shirt20_49 + twoSidesCost) 
                xy = shirt20_49
            elif numOfShirt >= 50 and numOfShirt <= 99:
                x = (shirt50_99 + twoSidesCost) 
                xy = shirt50_99
            elif numOfShirt >= 100 and numOfShirt <= 249:
                x = (shirt100_249 + twoSidesCost) 
                xy = shirt100_249
            elif numOfShirt >= 250:
                x = (shirt250_plus + twoSidesCost)
                xy = shirt250_plus  
        s = 0
        if screens == 1:
            s = 50
        elif screens == 2:
            s = 80
        elif screens == 3:
            s = 100
        elif (screens >= 4):
            s = (screens * 30)
        
        g = 0
        if largeGraphic == 'Yes':
            g = 0.5
        
        c = 0
        if numOfColour > 1:
            c = numOfColour
        
        w = 0
        if whitePrint:
            w = c + 0.5
        
        addOnTotal = 0
        if 'Puff Print' in addOns:
            addOnTotal += 1
        if 'Neck Prints' in addOns:
            addOnTotal += 3
        if 'Outsourced Labels' in addOns:
            addOnTotal += 1.5
        

        if whitePrint == 'Yes':
            equation = int((numOfShirt * x) + \
                        (numOfShirt * addOnTotal) + \
                        ((numOfShirt - int(whiteQuantity)) * c) + \
                        int((whiteQuantity) * w) + \
                        (numOfShirt * g) + (s))
            initialEquation = equation
            discount = 0
            if featuredArtist == 'Yes':
                discount = ((10/100) * equation)
                equation = equation - discount
        else:
            equation = int((numOfShirt * (x + c)) + (numOfShirt *
                                                    addOnTotal) + (numOfShirt * g) + (s))
            initialEquation = equation
            discount = 0
            if featuredArtist == 'Yes':
                discount = ((10/100) * equation)
                equation = equation - discount
        
        return x, xy, w, g, c, s, addOnTotal, initialEquation, equation, discount

    def printOut(cusSupply, featuredArtist, numOfShirt, garmentCost, x, xy, w, g, c, s, addOnTotal, initialEquation, equation, discount):

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Number of Shirts", numOfShirt)
            st.metric("Cost of Colours", c)
            st.metric("Customer Supply", cusSupply == "Yes")

        with col2:
            st.metric("Baseline Shirt Cost", xy)
            st.metric("Cost of Screens", s)
            st.metric("Returning Artist", featuredArtist == 'Yes')
            
        
        with col3:
            st.metric("Total Shirt Cost Price", x)
            st.metric("Total AddOns", addOnTotal)
            st.metric("Large Graphic", g == 0.5)

            
        # st.markdown("---")
        
        bottom_col_1, bottom_col_2 = st.columns(2)
        bottom_col_1.subheader("**Total Cost**: $" + str(initialEquation - discount))
        bottom_col_2.subheader("**Cost per Shirt**: $" + str(equation/numOfShirt))

        st.write("")

        with st.expander("**Summary**"):
            st.write(f"Number of Shirts: {numOfShirt:<10}")
            st.write(f"Returning Artist: {featuredArtist == 'Yes'!s:<10}")
            st.write(f"Baseline Shirt Cost: {xy:<10}")
            st.write(f"Total Shirt Cost Price: ${x:<10}")
            st.write(f"Large Graphic:    {g == 0.5!s:<10}")
            st.write(f"Total AddOns:     ${addOnTotal:<10}")
            st.write(f"Cost of Colours:  ${c:<10}")
            st.write(f"Cost of Screens:  ${s:<10}")
            st.write(f"Before Discount:  ${initialEquation:<10}")
            st.write(f"Discount Amount:  ${round(discount, 2):<10}")

        st.markdown("---")

    def customerForm():
        
        contact_form = """
        <form action="https://formsubmit.co/foxtrotprints@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name", placeholder = "Your Name" required>
            <input type="email" name="email", placeholder = "Your Email Address" required>
            <textarea name="message" placeholder="Paste 'Summary' Here!"></textarea>
            <input type="hidden" name="_next" value="https://jake-equinox-operation-foxtrot-generator-frontend-main-qg39s7.streamlit.app/">
            <button type="submit">Send</button>
        </form>
        """
        st.header("📬 Send A Quote!")

        form_text = """
        Instructions on Sending a Quote
        1. Complete the series of questions in the side-bar navigation.
        2. Expand the 'Summary' tab just above this header.
        3. Copy the 'Summary'.
        4. Paste the 'Summary' into the text field below.
        5. Hit 'Send' ❤️‍🔥
        
        """

        st.success(form_text)

        st.markdown(contact_form, unsafe_allow_html = True)
        Utilities.localCSS("style/style.css")

    def localCSS(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html = True)
        
    


def main():
    StreamLit.mainPage()

if __name__ == "__main__":
    main()