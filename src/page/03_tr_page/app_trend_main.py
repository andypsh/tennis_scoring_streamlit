from first_contents import FirstContents
from second_contents import SecondContents



def run_trend_main(data_loader):
   
    first_contents = FirstContents(data_loader)
    second_contents = SecondContents(first_contents)
    
if __name__ == "__main__":
    run_trend_main()

