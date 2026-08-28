# Spinning cube

To compile and run:

```bash
gcc -I -Wall -o cube main.c -lm && ./cube
```

Example:

```
         *.................*            
         ..                ..           
         . .               . .          
         .  .              .  .         
        .   .              .   .        
        .    .            .     .       
        .     .           .      .      
        .      *..................*     
        .      .          .       .     
        .      .          .       .     
       .       .          .       .     
       .       .          .      .      
       .      .           .      .      
       .      .           .      .      
       .      .           .      .      
       .      .          .       .      
      .       .          .       .      
      .       .          .      .       
      .       .          .      .       
      *..................*      .       
       .      .           .     .       
        .     .            .    .       
         .   .              .   .       
          .  .              .  .        
           . .               . .        
            ..                ..        
             *.................*        
                                        
                                        
Scaling: 1.000000
Rotation: x=20.000000, y=20.000000, z=0.000000
```

Keys:
- `q` = quit
- `o`, `p` = x-axis rotation
- `k`, `l` = y-axis rotation
- `n`, `m` = z-axis rotation
- `z`, `x` = scaling